#!/usr/bin/env node
/**
 * verify-plugin-bundle.mjs — Shopware plugin storefront bundle regression check.
 *
 * Run this against a built plugin bundle. It exits non-zero if the bundle replaces Shopware's
 * global plugin system, and (with --plugin/--selector) asserts the runtime contract too.
 *
 *   node verify-plugin-bundle.mjs --dist <dist>/js/<technical-name>
 *   node verify-plugin-bundle.mjs --dist <dist>/js/<technical-name> --plugin MyPlugin --selector '.js-my-toggle'
 *
 * The directory must contain the entry bundle named after the directory
 * (e.g. js/topdata-cart-recovery-s-w6/topdata-cart-recovery-s-w6.js) plus its chunk files.
 *
 * WHY IT EXISTS
 * -------------
 * A plugin that bundles a second copy of core's `plugin.manager` overwrites `window.PluginManager`
 * with an empty registry on every storefront page, breaking unrelated core plugins. Nothing in the
 * plugin's own feature fails, so this is easy to ship and hard to notice. This check fails on such
 * a bundle, which makes it a real regression test.
 */

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import process from 'node:process';

// ---------------------------------------------------------------- arg parsing

function parseArgs(argv) {
    const out = { dist: null, plugin: null, selector: null };

    for (let i = 0; i < argv.length; i++) {
        const key = argv[i];
        const value = argv[i + 1];

        if (key === '--dist') { out.dist = value; i++; }
        else if (key === '--plugin') { out.plugin = value; i++; }
        else if (key === '--selector') { out.selector = value; i++; }
        else if (key === '--help' || key === '-h') { out.help = true; }
        else { throw new Error(`unknown argument: ${key}`); }
    }

    return out;
}

const args = parseArgs(process.argv.slice(2));

if (args.help || !args.dist) {
    console.log(`usage: verify-plugin-bundle.mjs --dist <dist>/js/<technical-name> [--plugin <Name>] [--selector <sel>]`);
    process.exit(args.help ? 0 : 2);
}

// ---------------------------------------------------------------- static checks

const distDir = path.resolve(args.dist);

if (!fs.existsSync(distDir) || !fs.statSync(distDir).isDirectory()) {
    console.error(`FAIL  not a directory: ${distDir}`);
    console.error('      Build the storefront bundle first, or check the path.');
    process.exit(2);
}

const technicalName = path.basename(distDir);
const entryFile = path.join(distDir, `${technicalName}.js`);

if (!fs.existsSync(entryFile)) {
    console.error(`FAIL  entry bundle missing: ${entryFile}`);
    console.error('      Shopware looks for js/<technical-name>/<technical-name>.js exactly.');
    process.exit(2);
}

const jsFiles = fs.readdirSync(distDir).filter((f) => f.endsWith('.js'));
const sources = new Map(jsFiles.map((f) => [f, fs.readFileSync(path.join(distDir, f), 'utf8')]));

const failures = [];
const passes = [];

const pass = (msg) => { passes.push(msg); console.log(`OK    ${msg}`); };
const fail = (msg) => { failures.push(msg); console.error(`FAIL  ${msg}`); };

for (const [name, code] of sources) {
    for (const globalName of ['PluginManager', 'PluginBaseClass', 'PluginConfigManager']) {
        // assigning `window.X = ...` or `window.X=` in the minified bundle means we bundled core's
        // plugin system instead of using the global core already published
        const pattern = new RegExp(`window\\.${globalName}\\s*=[^=]`);
        if (pattern.test(code)) {
            fail(`${name} assigns window.${globalName} — it bundled a second copy of core's plugin system`);
        }
    }
}

if (failures.length === 0) {
    pass('no plugin-system globals are reassigned by the bundle');
}

// a clean bundle that externalised the base class should reference it, not inline deepmerge.
// Heuristic only - a plugin bundling a third-party lib is legitimately large, so this never fails.
const totalInlineBytes = [...sources.values()].reduce((n, c) => n + c.length, 0);
const sizeNote = `${Math.round(totalInlineBytes / 1024)} KiB across ${jsFiles.length} file(s)`;

if (totalInlineBytes > 60_000) {
    console.log(`NOTE  bundle is large (${sizeNote}) - fine if the plugin bundles a third-party lib, ` +
        'otherwise a core module is probably inlined');
} else {
    pass(`bundle size is plausible (${sizeNote})`);
}

// ---------------------------------------------------------------- runtime check

if (!args.plugin) {
    console.log('');
    console.log(`${passes.length} passed, ${failures.length} failed`);
    console.log('Pass --plugin/--selector for the runtime check.');
    process.exit(failures.length ? 1 : 0);
}

// stub Shopware's plugin system, load the real bundle on top of it
const registrations = [];
const fetchCalls = [];

class NodeStub {}
class CorePluginBaseStub {
    constructor(el, options = {}, pluginName = false) {
        if (!(el instanceof NodeStub)) throw new Error('not a node');
        this.el = el;
        this._pluginName = pluginName || this.constructor.name;
        this.options = options;
        this._registerInstance();
        this.init();
    }

    _registerInstance() {
        this.el.__plugins.set(this._pluginName, this);
        CorePluginManagerStub.instances(this._pluginName).push(this);
    }

    init() {}
}
class CorePluginManagerStub {
    static map = new Map();

    static instances(name) {
        if (!this.map.has(name)) this.map.set(name, []);
        return this.map.get(name);
    }

    register(name, plugin, selector) { registrations.push({ name, plugin, selector }); }

    getPlugin(name) {
        if (!this.constructor.map.has(name)) return new Map([['instances', []]]);
        return new Map([['instances', this.constructor.instances(name)]]);
    }

    getPluginInstancesFromElement(el) { return el.__plugins; }
}

let sandbox;

function loadChunk(node) {
    const file = path.join(distDir, node.src.split('/').pop());

    if (!fs.existsSync(file)) {
        node.onerror({ type: 'error', target: node });
        return;
    }

    vm.runInContext(fs.readFileSync(file, 'utf8'), sandbox, { filename: file });
    node.onload({ type: 'load', target: node });
}

sandbox = {
    console,
    Promise,
    setTimeout,
    clearTimeout,
    setImmediate,
    NodeStub,
    CorePluginBaseStub,
    CorePluginManagerStub,
    fetch: (url, opts) => {
        fetchCalls.push({ url, opts });
        return Promise.resolve({ ok: true });
    },
    document: {
        head: { appendChild: loadChunk },
        getElementsByTagName: () => [],
        getElementsByClassName: () => [],
        querySelectorAll: () => [],
        createElement: () => ({ setAttribute() {} }),
        currentScript: {
            tagName: 'SCRIPT',
            src: `https://shop.test/storefront/js/${technicalName}/${technicalName}.js`,
        },
    },
};
sandbox.window = sandbox;
sandbox.self = sandbox;
sandbox.globalThis = sandbox;
sandbox.window.PluginManager = new CorePluginManagerStub();
sandbox.window.PluginBaseClass = CorePluginBaseStub;

vm.createContext(sandbox);

const corePluginManager = sandbox.window.PluginManager;
const corePluginBase = sandbox.window.PluginBaseClass;

try {
    vm.runInContext(sources.get(`${technicalName}.js`), sandbox, { filename: entryFile });
} catch (err) {
    fail(`loading the entry bundle threw: ${err.message}`);
    process.exit(1);
}

if (sandbox.window.PluginManager !== corePluginManager) {
    fail('the bundle replaced window.PluginManager — this breaks every core storefront plugin');
} else {
    pass('window.PluginManager identity preserved after load');
}

if (sandbox.window.PluginBaseClass !== corePluginBase) {
    fail('the bundle replaced window.PluginBaseClass');
} else {
    pass('window.PluginBaseClass identity preserved after load');
}

const mine = registrations.filter((r) => r.name === args.plugin);

if (mine.length !== 1) {
    fail(`expected exactly 1 registration for ${args.plugin}, found ${mine.length}`);
} else {
    pass(`${args.plugin} registered on "${mine[0].selector}"`);
}

if (args.selector && mine[0] && mine[0].selector !== args.selector) {
    fail(`selector mismatch: registered "${mine[0].selector}", expected "${args.selector}"`);
}

const run = async () => {
    if (mine.length === 1) {
        const PluginClass = (await mine[0].plugin()).default;

        if (Object.getPrototypeOf(PluginClass) !== CorePluginBaseStub) {
            fail(`${args.plugin} does not extend core's PluginBaseClass`);
        } else {
            pass(`${args.plugin} extends core's PluginBaseClass`);
        }

        // exercise the instance so registration on the element is proven too
        const listeners = {};
        const el = new NodeStub();
        el.dataset = { url: 'https://shop.test/x' };
        el.__plugins = new Map();
        el.addEventListener = (evt, cb) => { listeners[evt] = cb; };

        try {
            const instance = new PluginClass(el, {}, args.plugin);

            if (el.__plugins.get(args.plugin) !== instance) {
                fail('instance was not registered on the element');
            } else {
                pass('instance registered on the element via the core registry');
            }

            if (listeners.change) {
                listeners.change({ target: { checked: true } });
                await new Promise((r) => setImmediate(r));

                if (!fetchCalls.length) {
                    console.log(`NOTE  no fetch() call on a "change" event — if this plugin posts, ` +
                        'check the X-Requested-With header is present');
                }
            }
        } catch (err) {
            fail(`constructing ${args.plugin} threw: ${err.message}`);
        }
    }

    console.log('');
    console.log(`${passes.length} passed, ${failures.length} failed`);

    if (failures.length) {
        console.error('');
        console.error('Fix: use the globals Shopware publishes instead of importing core modules —');
        console.error('  window.PluginManager.register(...)   instead of  import from src/plugin-system/plugin.manager');
        console.error('  class X extends window.PluginBaseClass instead of  import from src/plugin-system/plugin.class');
        console.error('  fetch() instead of src/service/http-client.service');
        console.error('See the sw67-storefront-plugin-bundle skill. For a permanent guard, copy the');
        console.error('build/webpack.config.js from topdata-cart-recovery-sw6 — it fails the build');
        console.error('on any unmapped src/... import.');
    }

    process.exit(failures.length ? 1 : 0);
};

run().catch((err) => {
    console.error(`FAIL  ${err.message || err}`);
    process.exit(1);
});
