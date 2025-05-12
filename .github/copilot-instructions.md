**Documentation Instructions**

append and save to the file codechanges-log.md on the folder copilot_documents all major changes to the solution, add a timestamp on each entry

append and save the history of our chat to the chat-history.md file on the folder copilot_documents, add a timestamp on each entry

**Code-generation instructions**

follow python PEP guidelines

use type declaration for functions return and parameters

**Test Generatios instructions**

generate test when user requests t

name tests using the format Should{expected result}Given{input data or action} where the words in {} depend on each test

build the solution before running tests

run a coverge addin while running tests

after every new test passes add changed files to git and commit

**Commit message generation instructions**

undate the documentation instructions before commit

before commiting always check for code duplication and delete duplicated code

before committing changes check if the changed code runs
After modifying the code and any other asset provide a short and context specific for generating commit messages

**Pull request title and description generation instructions**

write a title with a short summary of the mayor changes to the solution

wirte a body describing: What changes were made and significan design decisions made
