# Go Coding Conventions

## General

- **Go version**: 1.21+
- **Style**: Follow the standard Go formatting rules (use `go fmt`)
- **Documentation**: All exported functions, types, and constants must be documented
- **Naming**:
  - Use `camelCase` for variable and function names
  - Use `PascalCase` for exported (public) functions, types, and variables
  - Use `snake_case` for file names
  - Keep package names short, concise, and lowercase (e.g., `http`, `io`)
- **Error handling**: Explicit error handling with proper checks
- **Imports**: Group imports in the following order with a blank line between groups:
  1. Standard library imports
  2. Third-party imports
  3. Local package imports

## Project Structure

- Follow the standard Go project layout:
  ```
  project-name/
  ├── cmd/                  # Command-line applications
  │   └── app-name/         # Main application entry point
  ├── internal/             # Private code
  │   ├── pkg1/
  │   └── pkg2/
  ├── pkg/                  # Public libraries
  ├── api/                  # API definitions
  ├── configs/              # Configuration files
  ├── scripts/              # Build and utility scripts
  ├── docs/                 # Documentation
  ├── go.mod                # Module definition
  └── go.sum                # Dependencies checksum
  ```
- Place `main.go` files in the `cmd/<app-name>/` directory
- Use `internal/` for code not meant to be imported by other projects

## Testing

- **Unit tests**: Required for all new functionality
- Write tests in `_test.go` files alongside the code they test
- Use table-driven tests for testing multiple inputs/outputs
- Aim for at least 80% test coverage
- Use testify for more expressive assertions when needed

## Dependencies

- Keep dependencies minimal and justified
- Prefer standard library solutions when possible
- Use go modules for dependency management
- Commonly used libraries/frameworks:
  - **chi** or **gin**: For HTTP routing
  - **cobra**: For CLI applications
  - **viper**: For configuration management
  - **zap** or **logrus**: For structured logging
  - **sqlx** or **gorm**: For database operations

## Error Handling

- Return errors rather than using panic
- Use meaningful error messages
- Consider using error wrapping: `fmt.Errorf("doing something: %w", err)`
- Create custom error types for specific error cases
- Check errors immediately after function calls

## Concurrency

- Use goroutines judiciously
- Always use channels or sync package primitives to coordinate goroutines
- Consider using errgroup for managing groups of goroutines
- Avoid global variables for shared state
- Prefer mutex over channels for simple state protection

## Configuration

- Use environment variables for configuration
- Support both JSON and YAML for configuration files
- Implement validation for configuration values
- Provide sensible defaults

## Example go.mod

A minimal working example:

```go
// go.mod
module github.com/yourusername/your-project-name

go 1.21

require (
    github.com/go-chi/chi/v5 v5.0.10
    github.com/spf13/viper v1.16.0
    go.uber.org/zap v1.26.0
)
```
