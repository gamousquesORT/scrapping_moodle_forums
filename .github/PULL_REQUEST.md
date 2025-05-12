# Feature: Team Score Visualization and UI Modularization

## Changes Made
- Added team score visualization with current/maximum score display
- Separated UI code into focused, single-responsibility modules
- Standardized menu options across all interfaces
- Added folder existence checks with auto-creation
- Improved error handling for missing files

## Design Decisions
- Created ui package with separate modules:
  - input_validator.py: Centralized input validation logic
  - score_change.py: Dedicated class for tracking score changes
  - file_handler.py: Encapsulated file I/O operations
  - menu_handler.py: Standardized menu interactions
  - quiz_input_handler.py: Quiz parameter management
  - score_editor.py: Score editing and visualization
- Used dataclass for ScoreChange to ensure consistent score change tracking
- Maintained consistent menu structure with "Proceed" as first option
- Improved error handling with user-friendly messages

## Testing
- [x] Verified all UI modules function correctly
- [x] Tested team score visualization feature
- [x] Confirmed proper menu standardization
- [x] Validated input/output folder handling
- [x] Tested score editing and tracking functionality

## Additional Notes
- Improved code organization and maintainability
- Enhanced user experience with clear error messages
- Maintained backwards compatibility with existing features
- All changes follow Python PEP guidelines
