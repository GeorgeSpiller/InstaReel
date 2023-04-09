# INFO
This project ses various AI platforms to render video shorts from a given instagram post. It currently only works on posts form a specific instagam account, where descriptions are well-defined and follow a more or less constant format, eg:
https://www.instagram.com/p/CqiLin5piVy/
in the future, it will be refactored and simplified to be more general purpose.

# REFACTOR
This project will be refactored once decent image-to-text api's exist. Currently it scrapes the insta post for image descriptions, as this project focuses on a very specific use case. To generalise this use case however, in the future it can be simplified and itsscope broadened:
- Remove all image scraping and/or processing
- instead of taking instagram post description at face value, add it to GPT prompt to para-phrase (hopefully this should remove image descriptions, hashtags, and other description bloat).
- use an image-to-text ai to instead get the image descriptions.










