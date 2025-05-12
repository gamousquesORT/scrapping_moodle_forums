# Description

## Changes Made
- Added score editing functionality before quiz processing
- Implemented team selection by number instead of typing full team name
- Added score change tracking system with running history
- Enhanced user interface with clearer menus and validation
- Added confirmation steps for changes

## Design Decisions
- Used sorted team list for consistent numbering
- Stored complete change history with original and new scores
- Added +/- indicators to show score differences clearly
- Implemented final confirmation step with change summary
- Maintained data consistency by updating all team members' scores

## Testing
- [x] Manual testing completed with sample quiz data
- [x] Verified team selection by number functionality
- [x] Tested multiple score changes and history tracking
- [x] Confirmed proper validation of inputs
- [x] Validated final output file generation

## Additional Notes
- All changes follow Python PEP guidelines
- Maintains code modularity and separation of concerns
- Improves user experience with clear feedback and validation
- Changes are backwards compatible with existing quiz files