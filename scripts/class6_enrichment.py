# -*- coding: utf-8 -*-
"""Class 6 content patches + scaffolding (reviewable content, applied by fix_class6.py).

Every patch is anchored to (unit_id, section_id, block_index) and verified against
the expected old text before it is applied, so a mis-aligned patch fails loudly
instead of corrupting content.
"""

# ---------------------------------------------------------------------------
# 1. Global exact-string substitutions applied to every string in the JSON.
# Each tuple: (old, new, minimum_expected_count). Counts are asserted.
# ---------------------------------------------------------------------------
GLOBAL_SUBS = [
    # OCR watermark fragments of the publisher name ("Asmita") are handled by
    # regex below; these are the remaining literal cleanups.
    ("Os and 1s", "0s and 1s", 1),
    ("PRINT, INPUT LET", "PRINT, INPUT, LET", 1),
    (" 980 PRO", "", 1),
    ("PCle 4.0NVMeM2 2TB ", "", 1),
    ("permanently. A digital computer", "A digital computer", 1),
    ("SsD (Solid State Drive) is high speed ash-based memory device.",
     "SSD (Solid State Drive) is a high-speed flash-based memory device.", 1),
    ("UsB", "USB", 1),
    ("GUl ", "GUI ", 1),
    ("lnternet", "Internet", 1),
    ("lnformation", "Information", 1),
    ("loT ", "IoT ", 1),
    ("Al, is a type", "AI, is a type", 1),
    ("() instead of REM", "' (apostrophe) instead of REM", 1),
    ("yahoosearch. com", "search.yahoo.com", 1),
    ("WwW (World Wide Web)", "WWW (World Wide Web)", 1),
    ("is an another example", "is another example", 1),
    ("resident viruses Having", "resident viruses. Having", 1),
    ("add bullets or numbering too", "add bullets or numbering to", 1),
    ("@ A cell is an intersection", "A cell is an intersection", 1),
    ("the older extension. XLS", "the older extension .XLS", 1),
    ("extension.XLS", "extension .XLS", 1),
    ("used in multimedia are text, image, audio, video,",
     "used in multimedia are text, image, audio, video, and animation.", 1),
    ("Assembly language:It", "Assembly language: It", 1),
    ("DIM b As STRING", "DIM b AS STRING", 1),
    ("e.g.; CLS", "e.g. CLS", 1),
    ("2 and 3 are operands", "1 and 2 are operands", 1),
    ("iCT", "ICT", 1),
    ("applications areas", "application areas", 1),
    ("To insert a Shapes, follow these steps:",
     "To insert a shape, follow these steps:", 1),
    ("Inserting pictures into is a great way",
     "Inserting pictures into your document is a great way", 1),
    ("main features of MS Paint include: and Fill Tools",
     "main features of MS Paint include:", 1),
    ("in a variety of file", "in a variety of file formats such as JPEG, PNG, BMP and GIF", 1),
    ("Repeat steps 5-6 to add more strokes",
     "Repeat these steps to add more strokes", 1),
    ("You can also apply new colors to a theme. You can also apply new colors to a theme.",
     "You can also apply new colors to a theme.", 1),
    # Private-use "bullet" left by the PDF extractor -> real bullet.
    ("\uf038", "• ", 1),
]

# Regex cleanups (pattern, replacement, minimum_expected_count).
GLOBAL_RES = [
    (r"(?<![A-Za-z])A?mita(?=[\s\".,;:!?])", "", 1),   # "mita"/"Amita" watermark bits
    (r"(?<![A-Za-z])A?mila(?=[\s\".,;:!?])", "", 1),   # "mila"/"Amila" watermark bits
    (r"(?<![A-Za-z])mil(?=[\s\".,])", "", 1),          # "mil" watermark bits
    (r"(?<![A-Za-z])mild(?=[\s\".,])", "", 3),         # "mild" watermark bits (exactly 3)
    (r"[ \t]{2,}", " ", 0),                            # collapse gaps left behind
    (r"\s+\"$", "\"", 0),
    (r"\s+\.$", ".", 0),
]

# ---------------------------------------------------------------------------
# 2. Section retitles (ids unchanged, so figure anchors keep working).
# ---------------------------------------------------------------------------
RETITLES = {
    ("unit-3", "solid-state-drive"): "Advantages of Solid State Drive (SSD)",
    ("unit-5", "d-sleep"): "Sleep, Shut Down and Restart",
    ("unit-11", "view-as-window-s"): "Starting Microsoft PowerPoint 2016",
    ("unit-14", "iot-enabled-cities"): "IoT-Enabled Cities (Smart Cities)",
}

# ---------------------------------------------------------------------------
# 3. Whole-block text replacements.
# {key: (unit, section, index, field, expect_substring, new_text)}
# ---------------------------------------------------------------------------
PATCH_TEXT = [
    ("unit-2", "introduction", 0, "text",
     "QR code, and scanner. Central Processing Unit",
     "Examples of input devices: keyboard, mouse, scanner, trackball, touchpad, joystick, bar code reader, digital camera, microphone, graphic digitizer, touch screen, and QR code reader. This chapter describes the most common ones."),
    ("unit-2", "output-unit", 7, "text",
     "The printer is a peripheral device",
     "The printer is a peripheral device used to print text, pictures and illustrations in permanent readable form. Some of the common printers are dot matrix printers, laser printers, and ink-jet printers."),
    ("unit-5", "logging-into-computer-system", 0, "text",
     "User must click on his/her username",
     "A user must click on his/her username and supply a password (optional) to log in to the Windows desktop. The login screen below shows how Windows 11 asks for the sign-in."),
    ("unit-5", "logging-into-computer-system", 1, "text",
     "Turning off the Computer",
     "From the power button on the login screen (or the Start menu) the user can put the computer to sleep, shut it down, or restart it. The three options are explained in the next section."),
    ("unit-5", "windows-accessories", 0, "text",
     "Windows accessories provide additional tools",
     "Windows accessories provide additional tools that include network connection, multimedia, painting, text editing tools, accessibility options for disabled persons, entertainment tools, and so on."),
    ("unit-7", "summary-at-a-glance", 3, "text",
     "Example: Google chrome",
     "Web browser is a user-based application software that allows a user to interact with and display the webpages. Example: Google Chrome, Microsoft Edge, Mozilla Firefox. A webpage is a document that you see when you use the internet. It usually contains all sorts of things like text, pictures, videos, and information about different topics like animals, sports, or games. A URL (Uniform Resource Locator) is a unique identifier used to locate a resource on the Internet. It is also referred to as a web address."),
    ("unit-9", "insert-a-symbol", 0, "text",
     "Symbols can be used to currency symbols",
     "Symbols such as ©, ®, arrows and currency symbols (₹, $, €) can be added to your documents to make them clearer and more professional. The steps to insert a symbol are:"),
    ("unit-9", "working-with-pictures", 0, "text",
     "Inserting pictures into",
     "Inserting pictures into your document is a great way to enhance your document and make it more visually appealing. You can also resize and position the picture as needed. You can also click and drag the picture to move it to a different location in the document."),
    ("unit-9", "inserting-shapes", 0, "text",
     "Microsoft Word includes a wide range of shapes",
     "Microsoft Word includes a wide range of shapes that you can use to enhance your documents, including rectangles, circles, arrows, stars, and more. You can also customize the color, line style, and other properties of the shape. To insert a shape, follow these steps:"),
    ("unit-10", "ms-excel", 0, "text",
     "MS Excel is a commercial distributed",
     "MS Excel is a commercial spreadsheet application developed and distributed by Microsoft Inc. Its application file name is EXCEL.EXE and its extension is *.XLSX (Microsoft Office 2016); the older extension .XLS was used up to MS Excel 2003. Note: the Microsoft application (MS Excel) is the most popular spreadsheet, so this chapter discusses the spreadsheet using MS Excel 2016. How to open MS Excel 2016?"),
    ("unit-11", "duplicate-selected-slides", 2, "text",
     "Themes are designs",
     "Themes are designs that can be applied to an entire presentation. They allow for maintaining consistency throughout the presentation. You can also apply new colors to a theme. To add themes:"),
    ("unit-12", "working-with-ms-paint", 24, "text",
     "MSPaint grade 6",
     "If you choose “Save As”, enter a file name for your drawing and select the file type you want to save it as (such as JPEG, PNG, BMP, etc.). Click on the “OK” button to save your drawing. Once your drawing is saved, click on the “File” menu again and select “Exit” to close MS Paint."),
    ("unit-15", "introduction", 0, "text",
     "Types of Programming Languages Different types",
     "Programs are written in programming languages. Different types of programming languages are used, from machine language at the lowest level to high-level languages such as QBASIC:"),
    ("unit-15", "elements-of-qbasic-programming", 0, "text",
     "Some major elements of QBASIC programming are",
     "A QBASIC program is built from small building blocks. Some major elements of QBASIC programming are: character set, keywords, data types, variables, constants, and operators, expressions and operands."),
    ("unit-15", "elements-of-qbasic-programming", 3, "text",
     "Variable A variable is an entity",
     "A variable is an entity that can be changed during the execution of the program. There are two types of variables in QBASIC: numeric and string variables. a. Numeric variable: in QBASIC a numeric variable can hold an integer, a long integer, a single-precision, or a double-precision value — for example 15 or –26."),
    ("unit-15", "elements-of-qbasic-programming", 4, "text",
     "Type of Numeric 15",
     "A variable name followed by a type-declaration symbol shows its type: % for integer, &amp; for long integer, ! for single precision, # for double precision, and $ for string. b. String variable: a string variable stores string data, that is, alphanumeric data. A string variable can store up to 32767 characters. A string variable name must have a dollar ($) sign as its last character, must begin with a letter, may contain letters, digits and periods, and must not be a reserved word such as PRINT."),
    ("unit-15", "statements-in-qbasic", 1, "text",
     "Types of Statements Declaration Statements",
     "There are three types of statements in QBASIC: declaration statements, assignment statements, and I/O (input/output) statements. They are described one by one below."),
    ("unit-15", "statements-in-qbasic", 6, "text",
     "It displays output on the screen",
     "The PRINT statement displays output on the screen. We can also use a question mark (?) instead of the PRINT statement. Syntax: PRINT [expression_list]. Example: PRINT “QBASIC PROGRAMMING”."),
    ("unit-6", "cyber-law-in-nepal", 0, "text",
     "Electronic Transaction Act, 2063",
     "The cyber law of Nepal is called the Electronic Transaction Act, 2063, enacted in 2063 B.S. (2008 A.D.). This legal framework on cybercrime and electronic evidence in Nepal mostly addresses crimes against electronic and financial transactions. This law provides provisions for punishing cyber criminals as per the severity of the crime."),
]

# ---------------------------------------------------------------------------
# 4. Single list-item replacements.
# (unit, section, block_index, item_index, expect_substring, new_item)
# ---------------------------------------------------------------------------
PATCH_ITEM = [
    ("unit-6", "applications-of-ict", 1, 0,
     "online classes and distance learning",
     "ICT in Education In education, ICT is studied as a major subject in schools and universities. It is used as a teaching tool in the sector of education, science, engineering, medicine, and other fields. It is used as a learning tool in practical classes as well. After COVID-19, we knew that online classes and distance learning are possible only by using ICT tools."),
    ("unit-9", "introduction", 0, 0,
     "Window's Icon + R",
     "Press the Windows key + R on the keyboard."),
    ("unit-9", "introduction", 0, 4,
     "Saving, and Opening a Document",
     "Click on a blank document to create a new document. Now, a blank document opens and you can prepare a document as per your requirement."),
    ("unit-10", "ms-excel", 1, 0,
     "view as Window's Icon",
     "Click on the Start button (the Windows icon at the bottom-left of the screen)."),
    ("unit-10", "ms-excel", 1, 2,
     "Window's Icon + R",
     "Press the Windows key + R on the keyboard."),
    ("unit-10", "ms-excel", 14, 3,
     "To sort from smallest to largest",
     "You can sort in reverse alphabetical order by choosing Sort Z to A in the list."),
    ("unit-10", "ms-excel", 14, 4,
     "Select a cell in the column you want to sort",
     "To sort from smallest to largest: select a cell in the column you want to sort (a column with numbers)."),
    ("unit-11", "view-as-window-s", 1, 0,
     "Window's Icon + R",
     "Press the Windows key + R on the keyboard."),
    ("unit-13", "application-areas-of-multimedia", 1, 1,
     "DVD-ROMs or",
     "Entertainment: Multimedia is highly used in the entertainment industry, especially to develop special effects in movies and animations, like VFX and 3D animation. Multimedia games are most popular during this decade and are now available on DVD-ROMs or online stores."),
    ("unit-15", "elements-of-qbasic-programming", 8, 0,
     "single precision integer",
     "Constant A constant is a fixed entity that does not change during the execution of the program. A constant may be a letter, number, or special character. There are two types of constants: a. Numeric constant: it has only numbers from 0 to 9. There are four types of numeric constants in QBASIC — integer, long integer, single precision, and double precision. Example: 33. b. String constant: a string constant accepts alphanumeric values (alphabets and numbers). A string constant can be of a maximum of 255 characters. A constant whose value remains unchanged throughout the whole program is called a symbolic constant. In QBASIC, CONST is used to declare a symbolic constant."),
]

# ---------------------------------------------------------------------------
# 5. Block deletions (pure OCR garbage with no recoverable content).
# ---------------------------------------------------------------------------
DELETE_BLOCKS = [
    ("unit-8", "antivirus-software", 1),      # H3 "Secureyour everybit" (ad slogan)
    ("unit-12", "working-with-ms-paint", 19), # P "Rotate *" fragment
]

# ---------------------------------------------------------------------------
# 6. Slice replacements: (unit, section, start, end_exclusive, expect_first_60,
#    new_blocks). Applied per section in descending order so indices stay valid.
# ---------------------------------------------------------------------------
REPLACE_SLICES = [
    # --- unit-2: move the chinwag summary out of Output Unit is done via MOVE;
    # nothing sliced here.

    # --- unit-3: RAM intro was lost; ROM section hides a RAM-vs-ROM table.
    ("unit-3", "introduction", 0, 1, "There are two types of RAM:",
     [
         {"type": "p", "text": "RAM (Random Access Memory) is a read-and-write primary memory. It is volatile, which means its contents are lost when the power is switched off. It holds data and instructions while they are being used or waiting to be processed."},
         {"type": "p", "text": "There are two types of RAM:"},
     ]),
    ("unit-3", "rom-read-only-memory", 2, 3, "RAM stands for Random Access Memory.",
     [
         {"type": "h3", "text": "Difference between RAM and ROM"},
         {"type": "table", "caption": "RAM vs ROM", "head": ["RAM", "ROM"],
          "rows": [
              ["RAM stands for Random Access Memory.", "ROM stands for Read Only Memory."],
              ["It allows both read and write operations.", "It allows only read operations."],
              ["It is volatile — data is lost when the power supply is switched off.", "It is non-volatile and used for permanent storage."],
              ["It stores data and instructions while they are being processed, waiting to be processed, and after processing, before the result goes to the output device.", "It stores the programs required for the operation of electronic devices."],
              ["Types of RAM are SRAM and DRAM.", "Types of ROM are PROM, EPROM, and EEPROM."],
          ]},
     ]),

    # --- unit-4: rebuild the incoherent opener + the flattened compare table.
    ("unit-4", "types-of-software", 0, 1, "application software. Types of Software",
     [
         {"type": "p", "text": "Software is a set of programs, which is used to give instructions to the hardware. It directs and guides the input, process, and output operations of a computer. Software can be categorized into two types:"},
         {"type": "list", "ordered": False, "items": [
             "<strong>System software</strong> — manages and controls the overall operations of the computer.",
             "<strong>Application software</strong> — solves the user's specific tasks and makes them easier.",
         ]},
     ]),
    ("unit-4", "application-software", 1, 3, "So, application software is specially prepared",
     [
         {"type": "p", "text": "So, application software is specially prepared to do specific tasks. Examples: MS Office package, Windows Media Player, iTunes, Microsoft Paint, and InDesign."},
         {"type": "h3", "text": "Difference between System Software and Application Software"},
         {"type": "p", "text": "The differences between application software and system software are presented in the following table:"},
         {"type": "table", "caption": "System software vs application software",
          "head": ["System Software", "Application Software"],
          "rows": [
              ["It is the interface between the application software and the system hardware. Thus, it is used for operating computer hardware.", "It is developed to solve the particular problem of the user. Thus, it is installed according to the user's requirements."],
              ["It is essential for the operation of computer hardware. Without system software, a computer cannot start properly.", "It is not essential for the operation of the computer. It is installed as per the user's demand."],
              ["It is capable of running the hardware on its own.", "It is not capable of running on its own; it needs system software for its operation."],
              ["Examples: MS Windows 11, Linux, device driver, Mac OS, Android, and antivirus.", "Examples: MS Office package, Windows Media Player, iTunes, Microsoft Paint, and InDesign."],
          ]},
     ]),

    # --- unit-5: calculator merged into accessories intro; paint/sound/wordpad/
    # media-player collapsed into one paragraph; power options are word salad.
    ("unit-5", "windows-accessories", 0, 1, "Windows accessories provide additional tools",
     [
         {"type": "p", "text": "Windows accessories provide additional tools that include network connection, multimedia, painting, text editing tools, accessibility options for disabled persons, entertainment tools, and so on."},
         {"type": "h3", "text": "Calculator"},
         {"type": "p", "text": "Tool used for simple and scientific calculation."},
     ]),
    ("unit-5", "windows-accessories", 3, 5, "Paint",
     [
         {"type": "h3", "text": "Paint"},
         {"type": "p", "text": "Image editing tool with features for creating and editing drawings."},
         {"type": "h3", "text": "Sound Recorder"},
         {"type": "p", "text": "Records sound and saves it in the computer."},
         {"type": "h3", "text": "WordPad"},
         {"type": "p", "text": "Text editing tool with more features than Notepad."},
         {"type": "h3", "text": "Media Player"},
         {"type": "p", "text": "Plays audio and video files."},
     ]),
    ("unit-5", "d-sleep", 0, 1, "Shuts down windows Closes all app",
     [
         {"type": "p", "text": "The power button offers three ways to stop working. They do different things, so choose the right one:"},
         {"type": "list", "ordered": False, "items": [
             "<strong>Sleep</strong> — puts the computer in a low-power state so that you can quickly resume your session. The screen goes dark but your work stays open.",
             "<strong>Shut down</strong> — closes all apps and turns off the PC completely, so that you can safely turn the computer off.",
             "<strong>Restart</strong> — shuts Windows down and then starts it again automatically. It is useful after installing updates or new software.",
         ]},
     ]),

    # --- unit-7: uses/positive/negative lists collapsed into one; search steps
    # are a run-on paragraph.
    ("unit-7", "use-of-the-internet", 1, 2, "The Internet provides effective communication",
     [
         {"type": "list", "ordered": True, "items": [
             "The Internet provides effective communication among us using instant messaging services (social networks), no matter where you are.",
             "It is the source of information and source for eBook and online contents that provides a huge boost to education for students.",
             "Online shopping and online banking have made everyday life less complex.",
             "You can get global news without relying on television or newspapers.",
         ]},
         {"type": "h3", "text": "Positive Impacts of the Internet on our Society"},
         {"type": "list", "ordered": True, "items": [
             "It is the source of information and source for entertainment, which provides a faster, cheaper, and easier medium of communication globally.",
             "It helps for easier searching and sharing of information.",
             "It supports email communication.",
             "It is the primary way of electronic payment using credit/debit cards, ATMs, online payment, smart cards, and online services like banking, shopping, and education, which require the Internet.",
             "It includes social networking for instant touch with friends and relatives.",
         ]},
         {"type": "h3", "text": "Negative Impacts of the Internet on our Society"},
         {"type": "p", "text": "The negative impacts of the Internet on our society are:"},
         {"type": "list", "ordered": True, "items": [
             "Internet is one of the sources of spreading malware/computer viruses, and also for stealing, modifying, or destroying data.",
             "Some criminals use the Internet to hack others' accounts for the purposes of stealing data or financial information.",
             "A person's personal and professional life can be disrupted by an addiction to social networking.",
             "Long periods of screen time can negatively affect our health and communication skills by causing insomnia, eye strain, anxiety and depression.",
         ]},
     ]),
    ("unit-7", "process-of-searching-required-information-from-t", 0, 2,
     "Step 1: Open any browser",
     [
         {"type": "steps", "title": "Searching the Internet, step by step", "items": [
             "<strong>Step 1:</strong> Open any browser on the computer connected to the Internet (for example, open Google Chrome).",
             "<strong>Step 2:</strong> Type the URL of the search engine (for example, www.google.com) in the address bar of the browser.",
             "<strong>Step 3:</strong> Write the keywords about the topic you are searching in the search box and click on Google Search (or press the Enter key on the keyboard).",
             "<strong>Step 4:</strong> The search engine will provide the list of links and details about the searched topic.",
             "<strong>Step 5:</strong> Click on the link and open the contents.",
         ]},
     ]),

    # --- unit-9: font dialog merged into select-text; underline merged into
    # italics steps; page color/border merged into the shapes list.
    ("unit-9", "select-text", 0, 1, "In MS Word 2016, you can select text",
     [
         {"type": "p", "text": "In MS Word 2016, you can select text by using the mouse or the keyboard. You can also select text or items that are in different places."},
         {"type": "h3", "text": "Font dialog box (Ctrl + D)"},
         {"type": "p", "text": "You can specify how you want text to appear by selecting options in the Font dialog box. The availability of some options depends on the languages that are installed and enabled for editing:"},
     ]),
    ("unit-9", "make-text-italics", 1, 2, "Click Italics (I) on the Home Tab",
     [
         {"type": "list", "ordered": True, "items": [
             "Click Italics (<em>I</em>) on the Home tab, in the Font group, OR keyboard shortcut CTRL+I.",
             "Click Italics (<em>I</em>) on the Home tab, in the Font group again to remove italics from the text that you selected, OR keyboard shortcut CTRL+I.",
         ]},
         {"type": "h3", "text": "Underline words and the spaces between them"},
         {"type": "list", "ordered": True, "items": [
             "Select the text that you want to underline.",
             "On the Home tab, in the Font group, click Underline. Or press CTRL+U. Note: to change the underline style or color, click the Font Dialog Box Launcher, click the Font tab, and then change the Underline style or Underline color setting.",
         ]},
     ]),
    ("unit-9", "inserting-shapes", 1, 2, "On the Insert tab, Click on the Shapes button",
     [
         {"type": "list", "ordered": True, "items": [
             "On the Insert tab, click on the Shapes button in the Illustrations group. The different types of shapes will appear.",
             "Click on the desired shape from the gallery.",
             "Drag the mouse by clicking the left button where you want to insert that shape. Then the selected shape will be inserted.",
         ]},
         {"type": "h3", "text": "Using Page Color and Page Border in the Document"},
         {"type": "p", "text": "Page color refers to the background color of a document or page in Microsoft Word. By default, the page color in Word is white, but you can change it to any other color or shade that you prefer. A page border is a decorative element that can be added to the edges of a page in Microsoft Word. It can be used to frame the content on a page, add visual interest, or give a document a more professional look."},
         {"type": "h3", "text": "To use Page Color in the document"},
         {"type": "list", "ordered": True, "items": [
             "On the Design tab, click on the Page Color button.",
             "Select the color of your choice. You can also insert an image by selecting Fill Effects, Picture and Select Picture.",
         ]},
         {"type": "h3", "text": "To use Page Border in the document"},
         {"type": "list", "ordered": True, "items": [
             "On the Design tab, click on the Page Borders button.",
             "Select the Settings, Style, Color, Width, Art, Apply to and click the OK button.",
         ]},
     ]),

    # --- unit-10: font steps split across a list and a paragraph; autofill
    # series table flattened; function catalog flattened; borders split.
    ("unit-10", "ms-excel", 3, 8, "Select the cell, range of cells",
     [
         {"type": "list", "ordered": True, "items": [
             "Select the cell, range of cells, text, or characters that you want to format.",
             "On the Home tab, in the Font group: <strong>a.</strong> To change the font, click the font that you want in the Font box. <strong>b.</strong> To change the font size, click the font size that you want in the Font Size box, or click Increase Font Size or Decrease Font Size until the size you want is displayed in the Font Size box. <strong>c.</strong> To change the font colour, click on the dropdown arrow of Font Color and select the appropriate colour.",
         ]},
         {"type": "h3", "text": "AutoFill data in the cells"},
         {"type": "p", "text": "For fast data entry, you can have MS Excel automatically repeat data or fill data automatically. To fill in a series of numbers, dates, or other built-in series items, use the fill handle (the small black square in the lower-right corner of the selection). When you point to the fill handle, the pointer changes to a black cross. You can then quickly fill cells in a range with a series of numbers or dates, or with a built-in series for days, weekdays, months, or years:"},
         {"type": "list", "ordered": True, "items": [
             "Select the first cell in the range that you want to fill.",
             "Type the starting value for the series.",
             "Type a value in the next cell to establish a pattern. For example, if you want the series 1, 2, 3, 4, 5…, type 1 and 2 in the first two cells. If you want the series 2, 4, 6, 8…, type 2 and 4. If you want the series 2, 2, 2, 2…, you can leave the second cell blank.",
         ]},
         {"type": "p", "text": "More examples of series that you can fill: when you fill a series, the selections are extended as shown in the following table. Items separated by commas are placed in individual cells."},
         {"type": "table", "caption": "AutoFill series examples", "head": ["Initial selection", "Extended series"],
          "rows": [
              ["1, 2, 3", "4, 5, 6, …"],
              ["9:00", "10:00, 11:00, 12:00, …"],
              ["Mon", "Tue, Wed, Thu, …"],
              ["Monday", "Tuesday, Wednesday, Thursday, …"],
              ["Jan", "Feb, Mar, Apr, …"],
              ["Jan, Apr", "Jul, Oct, Jan, …"],
              ["Jan-99, Apr-99", "Jul-99, Oct-99, Jan-00, …"],
              ["15-Jan, 15-Apr", "15-Jul, 15-Oct, …"],
          ]},
     ]),
    ("unit-10", "ms-excel", 11, 12, "Select the cells to apply borders",
     [
         {"type": "list", "ordered": True, "items": [
             "Select the cells to apply borders.",
             "Click on the dropdown arrow of the Format command in the Cells group on the Home tab.",
             "Click the Format Cells option. Then the Format Cells dialog box will appear.",
             "Click on the Border tab.",
             "Choose the appropriate line from the Style palette.",
             "Select the line colour by clicking on the dropdown arrow to the right of the Colour box.",
             "In the Border section, set the edges of the selection which need bordering by clicking the button which shows the relevant edge.",
             "Click on the OK button.",
         ]},
         {"type": "h3", "text": "To remove borders"},
         {"type": "list", "ordered": True, "items": [
             "Select the area with the border to remove.",
             "Open the Format Cells dialog box as described above.",
             "Click on the Border tab and click on the None option.",
         ]},
     ]),
    ("unit-10", "ms-excel", 18, 20, "Functions in MS Excel",
     [
         {"type": "p", "text": "MS Excel contains built-in, readymade formulas. A readymade formula is called a <strong>function</strong>. It allows performing calculations quickly and easily. MS Excel supports different types of functions, categorized according to the work they do. Some commonly used functions are discussed below:"},
         {"type": "table", "caption": "Commonly used functions", "head": ["Function", "What it does", "Syntax"],
          "rows": [
              ["SUM", "Adds all the numbers in a range of cells.", "SUM(number1, number2, …)"],
              ["PRODUCT", "Multiplies all the numbers in a range of cells.", "PRODUCT(number1, number2, …)"],
              ["MAX", "Returns the largest value in a set of values.", "MAX(number1, number2, …)"],
              ["MIN", "Returns the smallest number in a set of values.", "MIN(number1, number2, …)"],
              ["AVERAGE", "Returns the average (arithmetic mean) of the arguments.", "AVERAGE(number1, number2, …)"],
          ]},
         {"type": "p", "text": "Number1, number2, … are 1 to 255 numeric arguments for which you want the result. Examples of mathematical calculations — Example 1: calculate Total, Total Amount, VAT and Grand Total. Procedure:"},
     ]),

    # --- unit-11: start sequence spans two ragged sections; transition steps
    # and slideshow options are run-ons.
    ("unit-11", "introduction", 0, 2, "To Start Microsoft PowerPoint 2016",
     [
         {"type": "p", "text": "To start Microsoft PowerPoint 2016, click on the Start button and choose PowerPoint — or use the Run box method described in the next section. A blank presentation opens and you can prepare a presentation as per your requirement."},
     ]),
    ("unit-11", "view-as-window-s", 0, 1, "PowerPoint 2016 OR",
     [
         {"type": "p", "text": "You can also open PowerPoint from the Run dialog box:"},
     ]),
    ("unit-11", "slide-transition", 1, 2, "Select the slide where you want to apply transition",
     [
         {"type": "list", "ordered": True, "items": [
             "Select the slide where you want to apply the transition.",
             "Click the Transitions tab and choose the transition effect you want (or open the Transition dialog box for more options).",
             "To add a transition sound, click the arrow next to Transition Sound and choose a sound.",
             "To modify the transition speed, click the arrow next to Transition Speed and choose a speed.",
         ]},
     ]),
    ("unit-11", "slide-show-options", 1, 2, "Preview the slide show from the beginning",
     [
         {"type": "list", "ordered": True, "items": [
             "<strong>From Beginning</strong> — preview the slide show from the first slide.",
             "<strong>From Current Slide</strong> — preview the slide show from the current slide.",
             "<strong>Set Up Slide Show</strong> — choose how the show runs (which slides, manual or automatic advance).",
         ]},
     ]),

    # --- unit-12: opening section is screenshot-label soup; view/resize/crop/
    # rotate/save passages are mangled.
    ("unit-12", "opening-ms-paint", 0, 3, "The steps to open MS Paint are:",
     [
         {"type": "p", "text": "The steps to open MS Paint are:"},
         {"type": "list", "ordered": True, "items": [
             "In the search bar, type “Paint” and click on the “Paint” program that appears in the search results.",
             "Once you have opened MS Paint, you will see a blank canvas where you can start creating your own drawings and paintings.",
         ]},
     ]),
    ("unit-12", "working-with-ms-paint", 15, 19, "Viewing Drawing",
     [
         {"type": "p", "text": "Viewing a drawing. The steps to view drawings are:"},
         {"type": "list", "ordered": True, "items": [
             "Click on the View tab at the top of the MS Paint window.",
             "To zoom, click on “Zoom” and choose a level from the drop-down menu — this makes your drawing bigger or smaller as per your requirement. You can also turn on “Gridlines” to line up parts of your drawing, use the “Ruler” to measure things, or choose “Full Screen” to make your drawing take up the whole screen.",
         ]},
         {"type": "h3", "text": "Resizing a picture or part of it"},
         {"type": "p", "text": "The steps to resize a picture or part of it are:"},
         {"type": "list", "ordered": True, "items": [
             "Click on the “Resize” button, which looks like two arrows pointing in opposite directions.",
             "In the Resize and Skew window, choose to resize by percentage or by specific dimensions.",
             "If you choose specific dimensions, enter the width and height you want the picture to be.",
             "You can keep the picture's proportions by checking the box next to “Maintain aspect ratio”.",
             "Once you have entered the desired resize options, click on the “OK” button. If you resized only a part of the picture, click on the “Crop” button in the Ribbon to crop the picture to the selected area.",
         ]},
         {"type": "h3", "text": "Cropping a drawing"},
         {"type": "p", "text": "The steps to crop a drawing are:"},
         {"type": "list", "ordered": True, "items": [
             "Click on the “Select” tool in the Ribbon, which looks like a dotted square.",
             "Click and drag your mouse to select the area of the drawing that you want to keep.",
             "Click on the “Crop” button in the Ribbon, which looks like a pair of scissors. The area outside the selection is removed.",
         ]},
     ]),
    ("unit-12", "working-with-ms-paint", 20, 24, "Rotating the Object",
     [
         {"type": "p", "text": "Rotating the object. The steps to rotate the object are:"},
         {"type": "list", "ordered": True, "items": [
             "Select the object (drawing/picture).",
             "Click on the “Rotate” button, which looks like a circular arrow, and choose “Rotate right 90°” or “Rotate left 90°”.",
         ]},
         {"type": "h3", "text": "Saving the drawing and exiting from Paint"},
         {"type": "p", "text": "The steps to save the drawing and exit from Paint are:"},
         {"type": "list", "ordered": True, "items": [
             "Click on the “File” menu.",
             "Click on “Save” or “Save As” to save your drawing to your desired location. “Save As” (F12) lets you choose from all possible file types.",
             "Enter a file name and pick a type — save a simple drawing with lower quality for email or the web, or save with high quality to use on your computer or on the web.",
         ]},
     ]),

    # --- unit-13: advantages/disadvantages jumbled into one paragraph.
    ("unit-13", "advantages-and-disadvantages-of-multimedia", 0, 1,
     "The advantages and disadvantages of multimedia are as follows:",
     [
         {"type": "p", "text": "The advantages of multimedia are as follows:"},
         {"type": "list", "ordered": False, "items": [
             "It is easy and effective to use.",
             "It increases learning activities.",
             "It is very interactive and entertaining.",
         ]},
         {"type": "p", "text": "The disadvantages of multimedia are as follows:"},
         {"type": "list", "ordered": False, "items": [
             "It is a bit expensive, and requires some additional hardware and software components.",
             "It demands skilled professionals.",
         ]},
     ]),

    # --- unit-14: the smart-cities section lost its body text.
    ("unit-14", "iot-enabled-cities", 0, 1, "BUILDINGS",
     [
         {"type": "p", "text": "When IoT connects a whole city, it becomes a <strong>smart city</strong>. Sensors in buildings, streets, traffic lights and water pipes send information over the Internet, so the city can control traffic, save electricity and water, and keep people safe."},
         {"type": "p", "text": "Examples are street lights that switch on only when someone passes by, traffic signals that adjust themselves to the traffic, and buildings that control their own heating and cooling."},
     ]),

    # --- unit-15: interface steps merged; operators/relational/logical tables
    # flattened; example programs fragmented across garbage headings.
    ("unit-15", "introduction-to-qbasic", 6, 8, "After downloading and saving",
     [
         {"type": "p", "text": "After downloading QBASIC and saving it on your computer drive, open it with these steps:"},
         {"type": "list", "ordered": True, "items": [
             "Open Computer (This PC).",
             "Open the folder where you saved QBASIC.",
             "Double-click on QB.EXE (inside DOSBox).",
             "Click on Run — the QBASIC editor opens and you can write your program.",
         ]},
         {"type": "h3", "text": "Writing, running, saving and exiting"},
         {"type": "list", "ordered": True, "items": [
             "To write a program in QBASIC, click on File → New Program and write the program.",
             "After writing the program, press the F5 key of the keyboard to run the program.",
             "To save your file, click on File → Save and give the file a name.",
             "To open an existing file, click on File → Open, select the required file and click OK.",
             "To exit from QBASIC, click on File → Exit.",
         ]},
     ]),
    ("unit-15", "elements-of-qbasic-programming", 9, 13, "Types of Operator i. Arithmetic",
     [
         {"type": "p", "text": "An operator is a symbol which tells the computer to perform certain mathematical and logical calculations. There are four types of operators:"},
         {"type": "h3", "text": "i. Arithmetic operators"},
         {"type": "p", "text": "Arithmetic operators represent arithmetic operations such as addition, subtraction, multiplication and division:"},
         {"type": "table", "caption": "Arithmetic operators in QBASIC",
          "head": ["Operation", "Operator", "Example"],
          "rows": [
              ["Addition", "+", "5+5"],
              ["Subtraction", "−", "5−2"],
              ["Multiplication", "*", "5*5"],
              ["Division", "/", "6/2"],
              ["Integer division (gives the integer part)", "\\", "5\\3"],
              ["Modulus (gives the remainder)", "MOD", "5 MOD 3"],
              ["Exponent (power)", "^", "2^3"],
          ]},
         {"type": "h3", "text": "Order (hierarchy) of operations"},
         {"type": "p", "text": "When several operators appear together, QBASIC evaluates them in this order:"},
         {"type": "list", "ordered": True, "items": [
             "Exponential (^)",
             "Multiplication and division (*, /, \\, MOD)",
             "Addition and subtraction (+, −)",
         ]},
         {"type": "h3", "text": "Rules for arithmetic expressions"},
         {"type": "p", "text": "In addition to this hierarchy of operations, the following rules must be kept in mind in an arithmetic expression:"},
         {"type": "list", "ordered": False, "items": [
             "Two operators must not appear together. For example, C+-D and A/-C are not permitted.",
             "String constants and string variables should not be used in arithmetic expressions. For example, P+P$ is wrong.",
             "When brackets are used, they must be used in pairs — every left bracket must be matched with a right bracket.",
             "The denominator of an expression should not be zero.",
             "Within a given pair of parentheses, the natural hierarchy of operations applies.",
         ]},
         {"type": "h3", "text": "ii. Relational operators"},
         {"type": "p", "text": "Relational operators are used to compare two values. The result of the comparison is either true or false:"},
         {"type": "table", "caption": "Relational operators in QBASIC",
          "head": ["Operator", "Meaning", "Example"],
          "rows": [
              ["=", "Equal to", "A = B"],
              ["&lt;&gt;", "Not equal to", "A &lt;&gt; B"],
              ["&lt;", "Less than", "A &lt; B"],
              ["&gt;", "Greater than", "A &gt; B"],
              ["&lt;=", "Less than or equal to", "A &lt;= B"],
              ["&gt;=", "Greater than or equal to", "A &gt;= B"],
          ]},
         {"type": "h3", "text": "iii. Logical operators"},
         {"type": "p", "text": "Logical operators are used to combine two or more expressions and return a single value. The common logical operators are:"},
         {"type": "list", "ordered": False, "items": [
             "<strong>AND</strong> — conjunction: true only when both expressions are true.",
             "<strong>OR</strong> — disjunction: true when at least one expression is true.",
             "<strong>NOT</strong> — logical negation: reverses true and false.",
         ]},
         {"type": "h3", "text": "iv. String operator"},
         {"type": "p", "text": "The string operator is used to join (concatenate) two strings. It is written as a + (plus) sign. Example: A$ = B$ + C$, where B$ and C$ are strings."},
         {"type": "p", "text": "<strong>Expressions:</strong> an expression is a set of variables and constants with different operators, showing the relationship between constants and variables."},
         {"type": "p", "text": "<strong>Operands:</strong> the operator operates on the operands. Example: in 1+2, “+” is the operator, and 1 and 2 are operands."},
     ]),
    ("unit-15", "statements-in-qbasic", 3, 5, "CLS statement",
     [
         {"type": "h3", "text": "CLS statement"},
         {"type": "p", "text": "This statement is used to clear the output screen. Generally, it is used at the start of the program. Syntax: CLS."},
         {"type": "h3", "text": "INPUT statement"},
         {"type": "p", "text": "The INPUT statement is used to accept data from the keyboard while the program is running. Syntax: INPUT [prompt;] variable. Example: INPUT “ENTER RADIUS OF CIRCLE”, R."},
     ]),
    ("unit-15", "statements-in-qbasic", 7, 12, 'PRINT "QBASIC PROGRAMMING" Some examples',
     [
         {"type": "h3", "text": "Some example programs"},
         {"type": "p", "text": "Type these programs in the QBASIC editor and press <strong>F5</strong> to run them."},
         {"type": "code", "lang": "text", "runnable": False, "title": "Program to display your subject name",
          "text": "REM program to display your subject name\nCLS\nPRINT \"COMPUTER SCIENCE\"\nEND"},
         {"type": "code", "lang": "text", "runnable": False, "title": "Program to add two numbers",
          "text": "REM program to add two numbers\nCLS\nLET A = 10\nLET B = 5\nLET S = A + B\nPRINT \"Sum of two numbers = \"; S\nEND"},
         {"type": "code", "lang": "text", "runnable": False, "title": "Program to calculate the area of a square",
          "text": "REM program to calculate the area of a square\nCLS\nINPUT \"Enter length of side \"; L\nLET Area = L * L\nPRINT \"Area of square = \"; Area\nEND"},
         {"type": "code", "lang": "text", "runnable": False, "title": "Program to calculate the area of a circle",
          "text": "REM program to calculate the area of a circle\nCLS\nINPUT \"Enter radius of circle \"; R\nLET Area = 3.14 * R * R\nPRINT \"Area of circle = \"; Area\nEND"},
     ]),
]

# ---------------------------------------------------------------------------
# 7. Single-block insertions: (unit, section, position, [blocks]).
# ---------------------------------------------------------------------------
INSERT_BLOCKS = [
    ("unit-12", "working-with-ms-paint", 11,
     [
         {"type": "list", "ordered": True, "items": [
             "Click on the “Select” tool and drag your mouse over the part of the picture that you want to copy.",
             "Click on the “Copy” button, which looks like two sheets of paper.",
             "Click on the “Paste” button, which looks like a clipboard. The copied part appears on the canvas.",
         ]},
     ]),
]

# ---------------------------------------------------------------------------
# 8. New sections: (unit, position, section_dict). Positions are original
# indices; multiple inserts per unit are applied in ascending order.
# ---------------------------------------------------------------------------
NEW_SECTIONS = [
    ("unit-2", 99,
     {"id": "summary-at-a-glance", "number": "", "title": "Summary at a Glance",
      "page": None, "blocks": []}),
    ("unit-4", 99,
     {"id": "summary-at-a-glance", "number": "", "title": "Summary at a Glance",
      "page": None, "blocks": []}),
    ("unit-8", 0,
     {"id": "what-is-malware", "number": "", "title": "What is Malware?",
      "page": None, "blocks": [
          {"type": "p", "text": "Malware is a program or file that is harmful to a computer, computer network, or server. The main aim of malicious programs is to infect systems and networks in order to gain access to sensitive information. Malware disrupts the normal functioning of a computer and infects or destroys data."},
          {"type": "h3", "text": "Types of malware"},
          {"type": "list", "ordered": False, "items": [
              "<strong>Computer virus</strong> — a malicious program that attaches to another program or a document, and can replicate and spread on its system.",
              "<strong>Worm</strong> — malware that spreads by itself across networks, without attaching to another program.",
              "<strong>Trojan horse</strong> — malware hidden inside a program that looks useful or harmless.",
              "<strong>Ransomware</strong> — malware that locks the victim's files and demands payment to unlock them.",
              "<strong>Spyware</strong> — malware that secretly watches what the user does and steals information.",
          ]},
          {"type": "h3", "text": "How malware spreads"},
          {"type": "p", "text": "Malware usually spreads from a removable device like a pen drive, from downloading contents from unsecured websites, and from email attachments."},
          {"type": "h3", "text": "Symptoms of malware"},
          {"type": "p", "text": "The common symptoms of malware are: slow computer operation, unwanted deletion of files and programs, system crashes or freezing of the computer screen, random security warnings or pop-up ads, redirection to suspicious websites, and antivirus software that is automatically disabled."},
      ]}),
]

# ---------------------------------------------------------------------------
# 9. Block moves: (unit, from_section, [indices], to_section). Source indices
# are original; moved blocks are appended to the target in order.
# ---------------------------------------------------------------------------
MOVE_BLOCKS = [
    ("unit-2", "output-unit", [8, 9, 10], "summary-at-a-glance"),
    ("unit-4", "application-software", [3, 4], "summary-at-a-glance"),
]

# ---------------------------------------------------------------------------
# 10. Scaffolding: notes, key terms, objectives, revision cards, teaching plan.
# ---------------------------------------------------------------------------
SCAFFOLD = {
    "unit-1": {
        "key_terms": [
            {"term": "Computer", "meaning": "A fast electronic data processing device. It processes input data according to instructions and produces information as output."},
            {"term": "Data", "meaning": "Raw facts and figures which carry no meaning by themselves."},
            {"term": "Information", "meaning": "Refined, processed data that carries meaning — for example a class average."},
            {"term": "Input", "meaning": "The data and instructions given to a computer for processing."},
            {"term": "Process", "meaning": "The manipulation or calculation of data inside the computer."},
            {"term": "Output", "meaning": "The result produced by the computer after processing."},
            {"term": "GIGO", "meaning": "Garbage In, Garbage Out — wrong input gives wrong output, however accurate the computer is."},
            {"term": "Versatility", "meaning": "The ability to do many different kinds of tasks in different fields."},
            {"term": "Diligence", "meaning": "Working continuously on repetitive tasks without getting tired or bored."},
            {"term": "Automation", "meaning": "Carrying on with a task by itself once it has been instructed."},
        ],
        "learning_objectives": [
            "Define a computer and explain where the word comes from.",
            "Describe the input–process–output working cycle of a computer.",
            "Explain the five characteristics (features) of a computer.",
            "List the capabilities and limitations of a computer.",
            "Describe the major application areas of computers with examples.",
            "Distinguish data from information with a simple example.",
        ],
    },
    "unit-2": {
        "note": "Notes for Chapter 2 of the Class 6 book: computer hardware — input devices, the CPU and its three parts, memory, and output devices.",
        "key_terms": [
            {"term": "Hardware", "meaning": "The physical parts of a computer which can be touched — input devices, processing unit, memory, and output devices."},
            {"term": "Input device", "meaning": "A device used to enter data and programs into the computer, e.g. keyboard, mouse, touchpad, joystick, touch screen."},
            {"term": "CPU", "meaning": "Central Processing Unit — the brain of the computer; processes inputs and controls all operations."},
            {"term": "ALU", "meaning": "Arithmetic and Logic Unit — performs calculations and logical operations as directed by the CU."},
            {"term": "CU", "meaning": "Control Unit — regulates the flow of data in the processor; the nerve system of the computer."},
            {"term": "Register", "meaning": "A tiny high-speed memory place inside the CPU that holds data for immediate processing."},
            {"term": "Primary memory", "meaning": "Memory that holds programs and data temporarily (RAM) or permanently for booting (ROM); includes cache memory."},
            {"term": "Secondary memory", "meaning": "Non-volatile storage that keeps programs and data permanently, e.g. hard disk, CD, DVD, SSD."},
            {"term": "Softcopy output", "meaning": "Untouchable, temporary output such as the display on a monitor or sound from a speaker."},
            {"term": "Hardcopy output", "meaning": "Touchable, permanent output printed on paper by a printer or plotter."},
        ],
        "learning_objectives": [
            "Define computer hardware and name its four parts.",
            "Describe common input devices and what each one does.",
            "Explain the CPU and its three components (ALU, CU, registers).",
            "Distinguish primary memory from secondary memory with examples.",
            "Distinguish softcopy output from hardcopy output with examples.",
            "Compare CRT, LCD and LED monitors and name common printer types.",
        ],
    },
    "unit-3": {
        "note": "Notes for Chapter 3 of the Class 6 book: memory devices — RAM and ROM, and the secondary storage devices from hard disk to SSD.",
        "key_terms": [
            {"term": "RAM", "meaning": "Random Access Memory — volatile read-and-write primary memory; contents are lost when power is off."},
            {"term": "ROM", "meaning": "Read Only Memory — non-volatile primary memory that permanently stores start-up programs."},
            {"term": "Volatile memory", "meaning": "Memory whose contents disappear without power, e.g. RAM."},
            {"term": "Non-volatile memory", "meaning": "Memory that keeps its contents without power, e.g. ROM, hard disk, CD, SSD."},
            {"term": "Hard disk", "meaning": "The most common secondary storage device; uses metallic disks and stores up to a few TB."},
            {"term": "CD", "meaning": "Compact Disk — a circular optical disk storing about 700 MB of text, graphics, sound or video."},
            {"term": "DVD", "meaning": "Digital Versatile/Video Disk — an optical disk storing about 4.7 GB, mainly video, software and data."},
            {"term": "Memory card", "meaning": "Small portable storage for phones, cameras and tablets, e.g. SD and MicroSD cards."},
            {"term": "Pen drive", "meaning": "A portable USB flash memory device used to carry and transfer files."},
            {"term": "SSD", "meaning": "Solid State Drive — a fast flash-based drive with no moving parts; faster and tougher than a hard disk."},
        ],
        "learning_objectives": [
            "Distinguish primary memory from secondary memory with examples.",
            "Explain RAM and its two types (SRAM and DRAM).",
            "Explain ROM and its types (PROM, EPROM, EEPROM).",
            "Compare RAM and ROM on read/write, volatility and use.",
            "Describe secondary storage devices: hard disk, CD, DVD, memory card, pen drive and SSD.",
            "Choose a suitable storage device for a given purpose and capacity.",
        ],
    },
    "unit-4": {
        "note": "Notes for Chapter 4 of the Class 6 book: computer software — what software is, system software, and application software.",
        "key_terms": [
            {"term": "Software", "meaning": "A set of programs that gives instructions to the hardware and directs input, process and output."},
            {"term": "Program", "meaning": "A set of instructions that tells the computer to perform a task."},
            {"term": "System software", "meaning": "Hardware-oriented software that manages and controls the whole computer, e.g. operating system, device driver, antivirus."},
            {"term": "Operating system", "meaning": "The main system software that runs the computer, e.g. Windows, Linux, macOS, Android."},
            {"term": "Device driver", "meaning": "System software that lets the operating system talk to a hardware device."},
            {"term": "Application software", "meaning": "User-oriented software prepared for a specific task, e.g. MS Office, Media Player, MS Paint."},
            {"term": "User-oriented", "meaning": "Made for the user's task (application software) rather than for running the hardware."},
            {"term": "Hardware-oriented", "meaning": "Made for managing the hardware (system software) rather than for a user task."},
        ],
        "learning_objectives": [
            "Define software and explain what it does for the hardware.",
            "Classify software into system software and application software.",
            "Explain system software with at least three examples.",
            "Explain application software with at least three examples.",
            "Compare system software and application software on purpose, necessity and examples.",
        ],
    },
    "unit-5": {
        "note": "Notes for Chapter 5 of the Class 6 book: the operating system — Windows desktop, files and folders, and accessories.",
        "key_terms": [
            {"term": "Operating system", "meaning": "System software that acts as an interface between the user and the hardware and controls programs, memory and processes."},
            {"term": "Desktop", "meaning": "The workspace screen of Windows with the background, icons, Start menu and taskbar."},
            {"term": "Icon", "meaning": "A small graphical image that represents a command, file, program or web page."},
            {"term": "Recycle Bin", "meaning": "The place holding deleted files and folders until it is emptied or they are restored."},
            {"term": "Start menu", "meaning": "The menu giving access to programs, documents, help and settings."},
            {"term": "File", "meaning": "A named collection of data stored on the computer, e.g. a document or a picture."},
            {"term": "Folder", "meaning": "A container that holds files and other subfolders to keep work organized."},
            {"term": "Taskbar", "meaning": "The bar (usually at the bottom) holding the Start button, open programs, clock and system tray."},
            {"term": "Login", "meaning": "Signing in with a username and password to reach the Windows desktop."},
            {"term": "Accessory", "meaning": "A small extra tool of Windows such as Calculator, Notepad, Paint, WordPad or Media Player."},
        ],
        "learning_objectives": [
            "Define an operating system and state its primary objectives and functions.",
            "Identify the parts of the Windows desktop: background, icons, Start menu and taskbar.",
            "Explain the Recycle Bin, This PC, icons and the Pictures folder.",
            "Log in, and use Sleep, Shut down and Restart correctly.",
            "Create, open, copy, cut, paste, rename and delete files and folders.",
            "Name Windows accessories and state what each one is used for.",
        ],
    },
    "unit-6": {
        "note": "Notes for Chapter 6 of the Class 6 book: ICT in education and daily life, and cyber law in Nepal.",
        "key_terms": [
            {"term": "ICT", "meaning": "Information and Communication Technology — tools and resources used to transmit, store, create, share or exchange information."},
            {"term": "E-commerce", "meaning": "Buying and selling goods and services over the Internet."},
            {"term": "Core banking software", "meaning": "The software banks use to replace manual records and handle transactions centrally."},
            {"term": "Cyber law", "meaning": "The legal provision for issues in cyberspace — also called the law of the Internet and computing."},
            {"term": "Cyberspace", "meaning": "The online world of the Internet and computers where digital activity happens."},
            {"term": "Cybercrime", "meaning": "A crime committed through computers or the Internet, e.g. hacking or data theft."},
            {"term": "Electronic Transaction Act, 2063", "meaning": "The cyber law of Nepal (2008 A.D.), punishing cyber criminals as per the crime."},
            {"term": "Intellectual property", "meaning": "Creations of the mind — writings, software, designs — protected by law."},
            {"term": "Digital signature", "meaning": "An electronic mark that proves who approved a digital document."},
            {"term": "Privacy", "meaning": "The right to keep one's personal information protected and controlled."},
        ],
        "learning_objectives": [
            "Define ICT and explain how it improves learning and teaching.",
            "List the advantages of ICT in education with examples.",
            "Describe application areas of ICT: education, banking, business, communication and entertainment.",
            "Define cyber law and name the five areas it covers.",
            "Explain the Electronic Transaction Act, 2063 as the cyber law of Nepal.",
            "Give examples of how cyber law protects users of the Internet.",
        ],
    },
    "unit-7": {
        "note": "Notes for Chapter 7 of the Class 6 book: the Internet, the web, browsers and search engines, and email.",
        "key_terms": [
            {"term": "Internet", "meaning": "The world's largest computer network — a network of networks."},
            {"term": "ISP", "meaning": "Internet Service Provider — a company selling Internet connections, e.g. Nepal Telecom, WorldLink, Vianet."},
            {"term": "World Wide Web", "meaning": "The giant collection of information (web pages) accessed through the Internet; invented by Tim Berners-Lee."},
            {"term": "Web browser", "meaning": "Application software used to view webpages, e.g. Chrome, Edge, Firefox, Safari."},
            {"term": "Webpage", "meaning": "A single document on the web — like one page of a book."},
            {"term": "Website", "meaning": "A collection of related webpages, e.g. YouTube; its first page is the homepage."},
            {"term": "URL", "meaning": "Uniform Resource Locator — the complete web address of a page."},
            {"term": "Search engine", "meaning": "Web software that finds information on the Internet, e.g. Google, Bing, DuckDuckGo."},
            {"term": "Email", "meaning": "Electronic mail — messages sent over the Internet, with optional attachments."},
            {"term": "Homepage", "meaning": "The first page of a website, opening when its address is typed."},
        ],
        "learning_objectives": [
            "Define the Internet and state its main uses.",
            "Explain the positive and negative impacts of the Internet on society.",
            "Distinguish the web, a website, a webpage and a URL.",
            "Define a web browser and name popular browsers.",
            "Search for information with a search engine step by step.",
            "Explain email, its address format, advantages and disadvantages.",
        ],
    },
    "unit-8": {
        "note": "Notes for Chapter 8 of the Class 6 book: computer malware — what it is, how it spreads, safe computing, and antivirus software.",
        "key_terms": [
            {"term": "Malware", "meaning": "Any program or file harmful to a computer, network or server."},
            {"term": "Virus", "meaning": "A malicious program that attaches to another program or document and replicates itself."},
            {"term": "Worm", "meaning": "Malware that spreads across networks by itself."},
            {"term": "Trojan horse", "meaning": "Malware disguised inside a program that looks useful or harmless."},
            {"term": "Ransomware", "meaning": "Malware that locks files and demands payment to release them."},
            {"term": "Spyware", "meaning": "Malware that secretly watches the user and steals information."},
            {"term": "Symptom", "meaning": "A visible sign of infection, e.g. slowness, crashes, pop-ups, disabled antivirus."},
            {"term": "Safe computing", "meaning": "Habits that stop malware: updated antivirus, firewall, scanning drives, safe downloads."},
            {"term": "Antivirus", "meaning": "Security software that prevents, detects and removes malware, e.g. McAfee, Kaspersky, Norton, AVAST."},
            {"term": "Firewall", "meaning": "A guard that controls what enters the computer from a network; keep it ON."},
        ],
        "learning_objectives": [
            "Define malware and name five types with one line on each.",
            "Explain how malware spreads between computers.",
            "List the common symptoms of a malware infection.",
            "Practise safe computing to prevent infection.",
            "Explain what antivirus software does and why updates matter.",
        ],
    },
    "unit-9": {
        "note": "Notes for Chapter 9 of the Class 6 book: word processing with MS Word 2016 — documents, formatting, lists, pictures and shapes.",
        "key_terms": [
            {"term": "Word processor", "meaning": "Application software for creating documents through text editing, formatting, storing and printing, e.g. MS Word."},
            {"term": "Document", "meaning": "A file created in a word processor — a letter, report, resume or article."},
            {"term": "Formatting", "meaning": "Changing how text looks: font, size, colour, style, alignment and effects."},
            {"term": "Font", "meaning": "The design of text characters, e.g. Arial or Times New Roman, with style and size."},
            {"term": "Alignment", "meaning": "How a paragraph sits on the page: left, center, right or justified."},
            {"term": "WordArt", "meaning": "Stylized decorative text with special colors, textures and shapes."},
            {"term": "Bulleted list", "meaning": "A list with bullet marks (•) instead of numbers."},
            {"term": "Numbered list", "meaning": "A list with numbers (1, 2, 3…) marking the order."},
            {"term": "Page border", "meaning": "A decorative frame added around the edges of a page."},
            {"term": "Save As", "meaning": "Saving a file with a new name, location or format."},
        ],
        "learning_objectives": [
            "Open MS Word 2016 and create a new document.",
            "Save, re-save (Save As), and open a document, including other formats.",
            "Format text: font, size, colour, bold, italic, underline, superscript and subscript.",
            "Align paragraphs and create bulleted and numbered lists.",
            "Insert WordArt, symbols, pictures and shapes into a document.",
            "Use page color and page borders to finish a document.",
        ],
    },
    "unit-10": {
        "note": "Notes for Chapter 10 of the Class 6 book: spreadsheet software with MS Excel 2016 — cells, formatting, formulas, functions, sorting and charts.",
        "key_terms": [
            {"term": "Spreadsheet", "meaning": "An application that organizes, analyzes and stores data in rows and columns, e.g. MS Excel."},
            {"term": "Cell", "meaning": "The intersection of a column and a row where data is stored; the first cell is A1."},
            {"term": "Cell address", "meaning": "A cell's location from its column letter and row number, e.g. B2, Z18."},
            {"term": "Cell range", "meaning": "A group of selected cells written with a colon, e.g. A1:A15."},
            {"term": "Active cell", "meaning": "The selected cell (thick border) that receives what you type."},
            {"term": "Worksheet", "meaning": "A single electronic sheet of rows and columns."},
            {"term": "Workbook", "meaning": "An Excel file holding one or more worksheets."},
            {"term": "Formula", "meaning": "A calculation starting with =, using values, references and operators."},
            {"term": "Function", "meaning": "A readymade formula such as SUM, PRODUCT, MAX, MIN or AVERAGE."},
            {"term": "Chart", "meaning": "A graphical presentation of worksheet numbers, e.g. column, line, pie or bar chart."},
        ],
        "learning_objectives": [
            "Explain the features of spreadsheet software and open MS Excel 2016.",
            "Define cell, cell address, range, active cell, worksheet and workbook.",
            "Format worksheet data: fonts, colours, AutoFill, borders and sorting.",
            "Write formulas that start with = and follow the rules for formulas.",
            "Use the SUM, PRODUCT, MAX, MIN and AVERAGE functions.",
            "Create a chart from worksheet data and change its type, size and position.",
        ],
    },
    "unit-11": {
        "note": "Notes for Chapter 11 of the Class 6 book: presentation software with MS PowerPoint 2016 — slides, text boxes, pictures, charts and shows.",
        "key_terms": [
            {"term": "Presentation software", "meaning": "Application software for creating visual presentations of ideas, e.g. PowerPoint, Google Slides."},
            {"term": "Slide", "meaning": "A single page of a presentation."},
            {"term": "Presentation", "meaning": "A sequence of slides with text, graphics, audio and video supporting a talk."},
            {"term": "Placeholder", "meaning": "A marked box on a slide layout waiting for a title, text or object."},
            {"term": "Theme", "meaning": "A ready design applied to a whole presentation for a consistent look."},
            {"term": "Transition", "meaning": "The visual movement when one slide changes to the next."},
            {"term": "Animation", "meaning": "Movement effects applied to objects on a slide (graphics, titles, bullets)."},
            {"term": "Slide show", "meaning": "Playing the presentation full-screen, from the beginning or the current slide."},
            {"term": "Chart", "meaning": "A graphical representation of data placed on a slide."},
            {"term": "Shape Fill", "meaning": "The colour filled inside a text box or shape."},
        ],
        "learning_objectives": [
            "Start PowerPoint 2016 and create a blank presentation.",
            "Resize, move, recolor and delete text boxes and placeholders.",
            "Add and duplicate slides and apply themes.",
            "Add pictures, shapes and charts to slides and edit chart data.",
            "Apply slide transitions and object animations with sound and timing.",
            "Run a slide show from the beginning or the current slide.",
        ],
    },
    "unit-12": {
        "note": "Notes for Chapter 12 of the Class 6 book: drawing with MS Paint — tools, colours, editing, and saving work.",
        "key_terms": [
            {"term": "MS Paint", "meaning": "A simple Windows drawing program for making and editing pictures."},
            {"term": "Canvas", "meaning": "The blank drawing area in the middle of the Paint window."},
            {"term": "Toolbar / Ribbon", "meaning": "The strip holding Paint's drawing and editing tools."},
            {"term": "Colour picker", "meaning": "The box for choosing the drawing or fill colour (Colour 1 / Colour 2)."},
            {"term": "Fill with Colour", "meaning": "The paint-bucket tool that fills a closed area with colour."},
            {"term": "Eraser", "meaning": "The tool that removes parts of a drawing like a virtual rubber."},
            {"term": "Select tool", "meaning": "The dotted-square tool for marking an area to copy, move or crop."},
            {"term": "Crop", "meaning": "Cutting a picture down to the selected area."},
            {"term": "Resize", "meaning": "Changing a picture's size by percentage or exact dimensions."},
            {"term": "Rotate", "meaning": "Turning a selected object, e.g. right 90° or left 90°."},
        ],
        "learning_objectives": [
            "Open MS Paint and identify its window components.",
            "Draw lines and shapes and fill areas with colour.",
            "Use the eraser, brush, text and selection tools.",
            "Copy, move, resize, crop and rotate parts of a drawing.",
            "Use the View tab: zoom, gridlines, ruler and full screen.",
            "Save a drawing in a suitable format and exit Paint.",
        ],
    },
    "unit-13": {
        "note": "Notes for Chapter 13 of the Class 6 book: multimedia — its five elements, advantages, disadvantages, and uses.",
        "key_terms": [
            {"term": "Multimedia", "meaning": "The combination of two or more media — text, image, audio, video, animation — working together."},
            {"term": "Text", "meaning": "Characters, words, sentences and paragraphs — the basic source of information."},
            {"term": "Graphics", "meaning": "Photographs, illustrations, drawings, clip art and icons."},
            {"term": "Audio", "meaning": "Sound effects, speech and music in a multimedia work."},
            {"term": "Video", "meaning": "Many related images with audio shown as a moving picture."},
            {"term": "Animation", "meaning": "Special visual movement or sound effects added to objects."},
            {"term": "VFX", "meaning": "Visual effects — computer-made imagery for movies and shows."},
            {"term": "Interactive", "meaning": "Letting the user navigate, respond and control — a key strength of multimedia."},
        ],
        "learning_objectives": [
            "Define multimedia and a multimedia system.",
            "Name and explain the five elements of multimedia with examples.",
            "List the advantages and disadvantages of multimedia.",
            "Describe application areas: education, entertainment, web, business and communication.",
            "Explain why multimedia suits teaching and entertainment.",
        ],
    },
    "unit-14": {
        "note": "Notes for Chapter 14 of the Class 6 book: contemporary technologies — e-commerce, online payment, cloud, AI, VR, mobile and IoT.",
        "key_terms": [
            {"term": "E-commerce", "meaning": "Buying and selling things using the Internet, e.g. Daraz, SastoDeal, MeroShopping."},
            {"term": "M-commerce", "meaning": "Commerce done on mobile devices like phones and tablets."},
            {"term": "Online payment", "meaning": "Paying or sending money over the Internet with a digital wallet or card."},
            {"term": "Cloud computing", "meaning": "Storing and using programs, files and data over the Internet from anywhere."},
            {"term": "Artificial intelligence", "meaning": "Technology that lets machines learn and decide like humans, e.g. voice assistants, game players."},
            {"term": "Virtual reality", "meaning": "A headset technology that places the user inside a virtual world."},
            {"term": "Mobile computing", "meaning": "Using technology on the go with phones, tablets and laptops."},
            {"term": "IoT", "meaning": "Internet of Things — everyday devices connected to the Internet and to each other."},
            {"term": "Smart city", "meaning": "A city using IoT sensors to manage traffic, lighting, water and safety."},
            {"term": "Social media", "meaning": "Internet services for sharing ideas through virtual networks and communities."},
        ],
        "learning_objectives": [
            "Define e-commerce and M-commerce with Nepali examples.",
            "Explain online payment and digital wallets.",
            "Explain cloud computing and its everyday uses.",
            "Describe AI and VR with two examples of each.",
            "Explain mobile computing and the Internet of Things.",
            "Describe how IoT makes a smart city work.",
        ],
    },
    "unit-15": {
        "note": "Notes for Chapter 15 of the Class 6 book: computer programming — language levels, QBASIC, its elements, statements, and example programs.",
        "key_terms": [
            {"term": "Program", "meaning": "A collection of instructions commanding the computer to perform a task."},
            {"term": "Programming", "meaning": "Writing a program following the grammar (rules) of a programming language."},
            {"term": "Machine language", "meaning": "First-generation language of 0s and 1s understood directly by the computer."},
            {"term": "Assembly language", "meaning": "Second-generation language using mnemonics (ADD, SUB, DIV) instead of binary."},
            {"term": "High-level language", "meaning": "Third-to-fifth generation languages in simple English-like statements, e.g. QBASIC, C, Java, Python."},
            {"term": "QBASIC", "meaning": "Quick Beginner's All-purpose Symbolic Instruction Code — a beginner's language by Microsoft (1985)."},
            {"term": "Statement", "meaning": "One instruction of a program; executable (acts) or non-executable (REM, DIM)."},
            {"term": "Variable", "meaning": "A named value that can change while the program runs (numeric or string)."},
            {"term": "Constant", "meaning": "A fixed value that never changes while the program runs (numeric or string)."},
            {"term": "Operator", "meaning": "A symbol telling the computer to calculate: arithmetic, relational, logical or string."},
        ],
        "learning_objectives": [
            "Define a program and programming, and classify programming languages by generation.",
            "Explain QBASIC: its full form, features, editor, and how to open, run, save and exit it.",
            "Identify the elements of QBASIC: character set, keywords, data types, variables and constants.",
            "Declare variables implicitly and explicitly (LET, DIM) with correct type symbols.",
            "Use arithmetic, relational, logical and string operators with correct hierarchy.",
            "Write, run and explain short QBASIC programs using REM, CLS, INPUT, PRINT, LET and END.",
        ],
    },
}

# Full replacement revision cards (unit-1 keeps its own).
QUICK_REVISION = {
    "unit-2": [
        {"title": "Hardware at a glance", "points": [
            "Hardware = physical parts you can touch.",
            "Four parts: input devices, CPU, memory, output devices.",
            "Data flows: input → process (CPU) → output, with memory holding data on the way."]},
        {"title": "Input and processing", "points": [
            "Input: keyboard, mouse, touchpad, joystick, touch screen, scanner, …",
            "CPU = brain: processes inputs and controls everything.",
            "CPU has 3 parts: ALU (calculates), CU (controls), registers (hold data)."]},
        {"title": "Memory and output", "points": [
            "Primary: RAM (temporary), ROM (permanent), cache.",
            "Secondary: hard disk, CD, DVD, SSD — permanent storage.",
            "Softcopy (screen, speaker) vs hardcopy (printer, plotter)."]},
        {"title": "Monitors and printers", "points": [
            "Monitor = most common softcopy device.",
            "Monitor types: CRT (bulky, old), LCD (flat), LED (modern).",
            "Printer = hardcopy device: dot matrix, ink-jet, laser."]},
    ],
    "unit-3": [
        {"title": "Two memory families", "points": [
            "Primary: holds programs + data during processing (RAM, ROM, cache).",
            "Secondary: permanent storage (hard disk, CD, DVD, SSD, pen drive).",
            "Volatile loses data without power (RAM); non-volatile keeps it."]},
        {"title": "RAM vs ROM", "points": [
            "RAM: read + write, volatile, holds work in progress.",
            "ROM: read only, non-volatile, holds start-up programs.",
            "RAM types: SRAM, DRAM. ROM types: PROM, EPROM, EEPROM."]},
        {"title": "Disks: hard, CD, DVD", "points": [
            "Hard disk: metallic disks, huge capacity (TB), inside the computer.",
            "CD: optical, ~700 MB — text, graphics, sound, video.",
            "DVD: optical, ~4.7 GB — mainly video, software, data."]},
        {"title": "Portable and modern", "points": [
            "Memory card: tiny storage for phones/cameras (SD, MicroSD).",
            "Pen drive: USB stick for carrying files between computers.",
            "SSD: flash-based, no moving parts — 10× faster reads than HDD."]},
    ],
    "unit-4": [
        {"title": "What software is", "points": [
            "Software = set of programs instructing the hardware.",
            "It directs input → process → output.",
            "Two kinds: system software and application software."]},
        {"title": "System software", "points": [
            "Hardware-oriented: runs and controls the computer.",
            "Examples: Windows, Linux, macOS, Android, device drivers, antivirus.",
            "Without it the computer cannot even start."]},
        {"title": "Application software", "points": [
            "User-oriented: does the user's specific task.",
            "Examples: MS Office, Media Player, MS Paint, Photoshop, Chrome.",
            "Installed as per the user's demand."]},
        {"title": "System vs application", "points": [
            "System = interface to hardware, essential, runs alone.",
            "Application = solves user problems, optional, needs system software.",
            "Exam favorite: give the 4-row comparison table from memory."]},
    ],
    "unit-5": [
        {"title": "OS basics", "points": [
            "OS = interface between user and hardware.",
            "Objectives: convenient to use + manage resources.",
            "Functions: I/O, process and memory management, security.",
            "Examples: Windows, macOS, Linux, Android, iOS."]},
        {"title": "Windows desktop", "points": [
            "Desktop: background + icons + Start menu + taskbar.",
            "This PC shows drives and hardware.",
            "Recycle Bin holds deleted items until emptied."]},
        {"title": "Login and power", "points": [
            "Log in with username + password.",
            "Sleep = low power, quick resume.",
            "Shut down = fully off; Restart = off and on again."]},
        {"title": "Files, folders, accessories", "points": [
            "Folder holds files and subfolders.",
            "Right-click for New / Copy / Cut / Paste / Rename / Delete.",
            "Accessories: Calculator, Notepad, Paint, WordPad, Media Player."]},
    ],
    "unit-6": [
        {"title": "ICT in short", "points": [
            "ICT = tools to transmit, store, create, share information.",
            "Improves learning, teaching, and student–teacher interaction.",
            "Covers education, banking, business, communication, entertainment."]},
        {"title": "ICT in education", "points": [
            "Easy sharing, motivated students, better IT literacy.",
            "Interesting classroom activities; online classes after COVID-19.",
            "Automates paper-based school procedures."]},
        {"title": "What cyber law is", "points": [
            "Law of the Internet and computing; fights cybercrime.",
            "Protects privacy, data, communication, IP, free speech.",
            "5 areas: computer crime, data protection, IP, digital signature, telecom."]},
        {"title": "Cyber law in Nepal", "points": [
            "Electronic Transaction Act, 2063 (2008 A.D.).",
            "Covers cybercrime and electronic/financial transactions.",
            "Punishes cyber criminals as per the crime; promotes IT growth."]},
    ],
    "unit-7": [
        {"title": "Internet essentials", "points": [
            "Internet = network of networks; world's largest network.",
            "ISPs in Nepal: NTC, WorldLink, Vianet, Subisu, CG Net, …",
            "Uses: information, email, communication, files, study, shopping, fun."]},
        {"title": "Impacts on society", "points": [
            "Positive: fast cheap communication, easy search/share, e-payment, e-learning.",
            "Negative: malware and hacking, addiction, health effects of screen time.",
            "Balance question — give two points on each side."]},
        {"title": "Web vocabulary", "points": [
            "WWW = giant collection of information (Tim Berners-Lee, 1989).",
            "Website = book; webpage = page; homepage = first page.",
            "URL = full web address. Browser = software to view pages.",
            "Search engine finds information: Google, Bing, …"]},
        {"title": "Email", "points": [
            "Electronic letter over the Internet, with attachments.",
            "Address form: name@example.com.",
            "Pros: paperless, free, fast, simple, anywhere.",
            "Cons: overload, malware in attachments, needs replies, less personal."]},
    ],
    "unit-8": [
        {"title": "Malware family", "points": [
            "Malware = harmful program/file attacking computers and networks.",
            "Types: virus, worm, Trojan horse, ransomware, spyware.",
            "Aim: infect systems and steal sensitive information."]},
        {"title": "Spread and symptoms", "points": [
            "Spreads via pen drives, unsafe downloads, email attachments.",
            "Symptoms: slow PC, deleted files, crashes, pop-ups, strange redirects.",
            "Disabled antivirus is itself a warning sign."]},
        {"title": "Safe computing", "points": [
            "Use certified antivirus and update it regularly.",
            "Keep the Windows firewall ON.",
            "Scan pen drives before use; download only from secure sites."]},
        {"title": "Antivirus", "points": [
            "Prevents, detects, searches and removes malware.",
            "Scans files, warns on detection, cleans infections, guards memory.",
            "Examples: McAfee, Kaspersky, Norton, AVAST."]},
    ],
    "unit-9": [
        {"title": "Word basics", "points": [
            "Word processor = software for creating documents (MS Word, …).",
            "Open: Start menu, or Windows key + R → WinWord.",
            "Save: CTRL+S. Save As: new name / place / format. Open: CTRL+O."]},
        {"title": "Formatting text", "points": [
            "Font dialog (CTRL+D): font, style, size, color, underline.",
            "B = bold (CTRL+B), I = italic (CTRL+I), U = underline (CTRL+U).",
            "Superscript (x²) and subscript (H₂O) from the Font group."]},
        {"title": "Paragraphs and lists", "points": [
            "Alignment: left, center, right, justified.",
            "Bulleted lists (•) and numbered lists (1, 2, 3…).",
            "Type * or 1 + SPACE to start a list automatically."]},
        {"title": "Objects and pages", "points": [
            "Insert: WordArt, symbols, pictures, shapes (Insert tab).",
            "Copy/cut/paste: CTRL+C / CTRL+X / CTRL+V.",
            "Finish with page color and page borders (Design tab)."]},
    ],
    "unit-10": [
        {"title": "Spreadsheet vocabulary", "points": [
            "Cell = column × row (first cell A1); range like A1:A15.",
            "Worksheet = one sheet; workbook = file of sheets.",
            "Active cell = selected cell with the thick border."]},
        {"title": "Excel basics", "points": [
            "MS Excel 2016: EXCEL.EXE, files end .XLSX.",
            "Open: Start menu, or Windows key + R → Excel.",
            "Features: organize data, easy calculation, charts."]},
        {"title": "Formulas and functions", "points": [
            "Formula starts with = (example: =C2*D2), press Enter.",
            "Not case sensitive; uses values, addresses, operators, functions.",
            "Functions: SUM, PRODUCT, MAX, MIN, AVERAGE."]},
        {"title": "Data tools", "points": [
            "Format: fonts, colours, AutoFill, printable borders.",
            "Sort A→Z / Z→A, smallest→largest and back.",
            "Charts: column, line, pie, bar, area, scatter — auto-update with data."]},
    ],
    "unit-11": [
        {"title": "Presentation vocabulary", "points": [
            "Slide = one page; presentation = sequence of slides.",
            "Made with: PowerPoint, Google Slides, Canva, Impress.",
            "Text boxes and placeholders hold titles, text and objects."]},
        {"title": "Building slides", "points": [
            "Start: Start menu, or Windows key + R → powerpnt.",
            "New slide (Office theme) or duplicate the selected slide.",
            "Themes keep the whole presentation consistent."]},
        {"title": "Content on slides", "points": [
            "Resize/move text boxes with corner and border handles.",
            "Insert pictures (Insert tab), shapes, and charts.",
            "Edit chart data from the Design tab."]},
        {"title": "Motion and show", "points": [
            "Transition = movement between slides; animation = movement on a slide.",
            "Add sound and speed to transitions.",
            "Slide show: from beginning, from current slide, or set-up show."]},
    ],
    "unit-12": [
        {"title": "Paint essentials", "points": [
            "MS Paint = simple Windows drawing program.",
            "Open: search “Paint” in the search bar.",
            "Parts: menu bar, toolbar/ribbon, drawing area, colour picker, shapes."]},
        {"title": "Drawing tools", "points": [
            "Shapes: line, rectangle, circle, arrow, …",
            "Fill with Colour (paint bucket) fills closed areas.",
            "Brush = freehand strokes; Eraser = virtual rubber.",
            "Text tool (A) adds text with font, size and colour."]},
        {"title": "Editing pictures", "points": [
            "Select tool marks areas to copy, move or crop.",
            "Resize by % or dimensions (keep aspect ratio).",
            "Crop cuts to the selection; Rotate turns 90° left/right.",
            "View tab: zoom, gridlines, ruler, full screen."]},
        {"title": "Saving work", "points": [
            "File → Save / Save As (F12); name the file.",
            "Formats: JPEG, PNG, BMP, GIF — quality vs size.",
            "File → Exit closes Paint after saving."]},
    ],
    "unit-13": [
        {"title": "Multimedia in short", "points": [
            "Multimedia = 2+ media at once: text, image, audio, video, animation.",
            "Idea: let the user navigate, interact, create, communicate.",
            "System = setup integrating the media types."]},
        {"title": "Five elements", "points": [
            "Text: characters, words, sentences, paragraphs.",
            "Image/graphics: photos, drawings, clip art, icons.",
            "Audio: speech, music, sound effects.",
            "Video: moving images + sound. Animation: movement/sound effects."]},
        {"title": "Pros and cons", "points": [
            "Pros: easy and effective, boosts learning, interactive fun.",
            "Cons: bit expensive (extra hardware/software), needs skilled people."]},
        {"title": "Where it is used", "points": [
            "Education: slides, assessments, self-learning.",
            "Entertainment: VFX, 3D animation, games.",
            "Web, business (ads, promotion) and communication (video chat)."]},
    ],
    "unit-14": [
        {"title": "Trade online", "points": [
            "E-commerce = buying/selling on the Internet (Daraz, SastoDeal, …).",
            "M-commerce = the same on phones and tablets.",
            "Online payment: digital money via wallets/cards for shopping or sending cash."]},
        {"title": "Cloud and AI", "points": [
            "Cloud = storage and programs on the Internet, reachable anywhere.",
            "Good for backup, sharing and group school projects.",
            "AI = machines that learn and decide: voice assistants, game players, art."]},
        {"title": "VR and mobile", "points": [
            "VR = headset worlds that feel real: games, travel, training.",
            "Mobile computing = phones/tablets/laptops on the go.",
            "IoT = everyday things connected: lights, appliances, alerts."]},
        {"title": "Smart cities", "points": [
            "IoT + city = smart city: sensors run traffic, lighting, water, safety.",
            "Examples: smart street lights, adaptive signals, smart buildings.",
            "Social media = sharing ideas through virtual communities."]},
    ],
    "unit-15": [
        {"title": "Language levels", "points": [
            "Machine language: 0s and 1s, 1st generation, hardest for humans.",
            "Assembly: mnemonics (ADD, SUB, DIV), 2nd generation.",
            "High-level: English-like, 3rd–5th generation (QBASIC, C, Java, Python)."]},
        {"title": "QBASIC basics", "points": [
            "QBASIC = Quick Beginner's All-purpose Symbolic Instruction Code (1985).",
            "Features: easy, auto syntax check, keeps variable names, capitalizes keywords.",
            "Editor: write, debug, run (F5), save (File → Save), exit (File → Exit)."]},
        {"title": "Elements", "points": [
            "Character set, keywords (CLS, PRINT, …), data (numeric/string).",
            "Variables change (% & ! # $); constants don't (CONST for symbolic).",
            "Declare implicitly (LET, at assignment) or explicitly (DIM … AS …)."]},
        {"title": "Operators and statements", "points": [
            "Operators: arithmetic (+ − * / \\ MOD ^), relational, logical, string (+).",
            "Order: ^ first, then * /, then + −; brackets in pairs.",
            "Statements: declaration (REM, CONST, DIM, END), assignment (LET, SWAP), I/O (CLS, INPUT, PRINT)."]},
    ],
}

# Full replacement teaching plans (unit-1 keeps its own).
TEACHING_PLAN = {
    "unit-2": [
        {"period": "Period 1", "topic": "Introduction — input devices",
         "activity": "Show real input devices (keyboard, mouse) and match each to the notes list; pupils name the inventor facts as a quiz.",
         "outcome": "Students can name input devices and describe the keyboard, mouse, touchpad, joystick and touch screen.", "figures": []},
        {"period": "Period 2", "topic": "Central Processing Unit",
         "activity": "Draw the CPU with ALU, CU and registers on the board; pupils explain one part each in their own words.",
         "outcome": "Students can explain the CPU and its three components.", "figures": []},
        {"period": "Period 3", "topic": "Memory Unit",
         "activity": "Build a two-column chart: primary (RAM, ROM, cache) vs secondary (hard disk, CD, DVD, SSD).",
         "outcome": "Students can distinguish primary from secondary memory with examples.", "figures": []},
        {"period": "Period 4", "topic": "Output Unit",
         "activity": "Sort flashcards into softcopy vs hardcopy; compare CRT/LCD/LED monitor pictures and printer types.",
         "outcome": "Students can classify outputs and compare monitors and printers.", "figures": []},
        {"period": "Period 5", "topic": "Summary + Exercise 2",
         "activity": "Rapid-fire revision of the summary, then pupils attempt objective and short questions in pairs.",
         "outcome": "Students can answer Exercise 2 questions on hardware.", "figures": []},
    ],
    "unit-3": [
        {"period": "Period 1", "topic": "Introduction + ROM",
         "activity": "Explain volatile vs non-volatile with a live demo (unsaved file vs saved file); complete the RAM-vs-ROM table together.",
         "outcome": "Students can compare RAM and ROM and name their types.", "figures": []},
        {"period": "Period 2", "topic": "Hard disk, CD and DVD",
         "activity": "Pass around a real hard disk and disks if available; pupils record capacity and use of each in a table.",
         "outcome": "Students can describe the hard disk, CD and DVD with capacities.", "figures": []},
        {"period": "Period 3", "topic": "Memory card, pen drive and SSD",
         "activity": "Show a memory card and pen drive; discuss why SSDs are replacing hard disks (speed, durability, power).",
         "outcome": "Students can describe portable and modern storage and SSD advantages.", "figures": []},
        {"period": "Period 4", "topic": "Summary + Exercise 3",
         "activity": "Memory-device quiz (which device for which job?), then short and long questions from Exercise 3.",
         "outcome": "Students can choose storage devices and answer Exercise 3.", "figures": []},
    ],
    "unit-4": [
        {"period": "Period 1", "topic": "Types of Software",
         "activity": "Define software; pupils sort example cards (Windows, MS Word, driver, game, antivirus…) into two columns.",
         "outcome": "Students can define software and classify it into two types.", "figures": []},
        {"period": "Period 2", "topic": "System Software",
         "activity": "Discuss why the computer cannot start without an OS; list the system software on the lab computers.",
         "outcome": "Students can explain system software with examples.", "figures": []},
        {"period": "Period 3", "topic": "Application Software + comparison table",
         "activity": "Name the application software pupils use daily; fill the 4-row system-vs-application table on the board.",
         "outcome": "Students can compare the two software types point by point.", "figures": []},
        {"period": "Period 4", "topic": "Summary + Exercise 4",
         "activity": "Recite the comparison table from memory, then answer Exercise 4 objective and short questions.",
         "outcome": "Students can answer Exercise 4 on software.", "figures": []},
    ],
    "unit-5": [
        {"period": "Period 1", "topic": "Components of Windows + Recycle Bin",
         "activity": "Tour the lab desktop: point out background, icons, Start menu, taskbar; delete and restore a practice file.",
         "outcome": "Students can identify desktop parts and use the Recycle Bin.", "figures": ["figures/class6/desktop-of-window-11.jpg", "figures/class6/various-icons-found-in-windows.jpg"]},
        {"period": "Period 2", "topic": "Start Menu + logging in + power options",
         "activity": "Pupils log in themselves, open programs from Start, then practise Sleep / Shut down / Restart on one machine.",
         "outcome": "Students can log in and choose the right power option.", "figures": ["figures/class6/start-menu.jpg", "figures/class6/login-screen-of-windows-11.jpg"]},
        {"period": "Period 3", "topic": "Files and folders",
         "activity": "Lab drill: create a folder, create/rename/copy/move/delete files inside it, step by step with the notes.",
         "outcome": "Students can manage files and folders with the mouse and keyboard.", "figures": []},
        {"period": "Period 4", "topic": "Windows Accessories + Summary + Exercise 5",
         "activity": "Open Calculator, Notepad, Paint, WordPad and Media Player; quick tour of each, then Exercise 5 questions and practicals.",
         "outcome": "Students can name accessories and answer Exercise 5.", "figures": []},
    ],
    "unit-6": [
        {"period": "Period 1", "topic": "Introduction + advantages of ICT in education",
         "activity": "List the ICT tools used in this school; pupils give one example per advantage from their own classes.",
         "outcome": "Students can define ICT and list its educational advantages.", "figures": []},
        {"period": "Period 2", "topic": "Applications of ICT",
         "activity": "Group task: each group presents one sector (education, banking, business, communication/entertainment).",
         "outcome": "Students can describe ICT uses in five sectors.", "figures": []},
        {"period": "Period 3", "topic": "Cyber law + cyber law in Nepal",
         "activity": "Discuss real cases (hacking, piracy, fraud); match each to an area of cyber law and to the ETA 2063.",
         "outcome": "Students can explain cyber law areas and Nepal's Electronic Transaction Act.", "figures": []},
        {"period": "Period 4", "topic": "Summary + Exercise 6",
         "activity": "Debate: “Is cyber law strong enough?” then answer Exercise 6 questions.",
         "outcome": "Students can answer Exercise 6 on ICT and cyber law.", "figures": []},
    ],
    "unit-7": [
        {"period": "Period 1", "topic": "Introduction + uses of the Internet",
         "activity": "Survey the class: who uses the Internet for what? Build the uses list, then split impacts into positive/negative columns.",
         "outcome": "Students can state Internet uses and impacts with examples.", "figures": []},
        {"period": "Period 2", "topic": "WWW, browser, URL, website + search engines",
         "activity": "Draw the book/web analogy; pupils dissect a real URL on the board and run a guided search step by step.",
         "outcome": "Students can use web vocabulary and search the Internet.", "figures": []},
        {"period": "Period 3", "topic": "Email: intro, advantages, disadvantages",
         "activity": "Write a class email address on the board; pupils label its parts and argue pros vs cons in two teams.",
         "outcome": "Students can explain email, addresses, advantages and disadvantages.", "figures": []},
        {"period": "Period 4", "topic": "Summary + Exercise 7",
         "activity": "Lab (if online): open a browser, search a topic, note the steps; then Exercise 7 questions.",
         "outcome": "Students can search the web and answer Exercise 7.", "figures": []},
    ],
    "unit-8": [
        {"period": "Period 1", "topic": "What is malware? + how it spreads + symptoms",
         "activity": "Tell the story of one infection (pen drive → slow PC → pop-ups); pupils match symptoms to the figure.",
         "outcome": "Students can define malware, name its types, and list spread routes and symptoms.", "figures": ["figures/class6/symptoms-of-malware.jpg"]},
        {"period": "Period 2", "topic": "Prevention + antivirus software",
         "activity": "Safe-computing checklist drill; open the lab antivirus, check its update date and run a quick scan demo.",
         "outcome": "Students can practise safe computing and explain antivirus tasks.", "figures": ["figures/class6/antivirus-softwares.jpg"]},
        {"period": "Period 3", "topic": "Summary + Exercise 8",
         "activity": "Symptom-or-not quiz, then Exercise 8 objective, short and long questions.",
         "outcome": "Students can answer Exercise 8 on malware.", "figures": []},
    ],
    "unit-9": [
        {"period": "Period 1", "topic": "Opening Word + saving and opening documents",
         "activity": "Lab: every pupil opens Word both ways, types their name, saves (CTRL+S), Save As with a new name, closes and reopens.",
         "outcome": "Students can open, save and reopen documents.", "figures": []},
        {"period": "Period 2", "topic": "Formatting text + paragraphs + lists",
         "activity": "Format-the-paragraph drill: font, B/I/U, superscript, alignment, then build one bulleted and one numbered list.",
         "outcome": "Students can format text, align paragraphs and create lists.", "figures": []},
        {"period": "Period 3", "topic": "WordArt, symbols, pictures, shapes, page design",
         "activity": "Make-a-poster task: title in WordArt, one symbol, one picture, one shape, page color and border.",
         "outcome": "Students can enrich a document with objects and page design.", "figures": []},
        {"period": "Period 4", "topic": "Summary + Exercise 9",
         "activity": "Finish posters; peer-review against a checklist, then Exercise 9 questions and practicals.",
         "outcome": "Students can produce a finished document and answer Exercise 9.", "figures": []},
    ],
    "unit-10": [
        {"period": "Period 1", "topic": "Features + fundamentals (cell → workbook)",
         "activity": "Open a blank workbook; pupils find A1, select ranges, rename a sheet, and name each part aloud.",
         "outcome": "Students can use cell, range, active cell, worksheet and workbook correctly.", "figures": []},
        {"period": "Period 2", "topic": "Formatting, AutoFill, borders, sorting",
         "activity": "Lab worksheet: format a small table, AutoFill a series, add borders, sort A→Z and back.",
         "outcome": "Students can format, fill, border and sort worksheet data.", "figures": []},
        {"period": "Period 3", "topic": "Formulas, functions, charts",
         "activity": "Build the Total/Amount/VAT sheet from the notes (=C2*D2, =SUM(E2:E6)); add MAX/MIN/AVERAGE; insert a column chart.",
         "outcome": "Students can calculate with formulas and functions and chart results.", "figures": []},
        {"period": "Period 4", "topic": "Summary + Exercise 10",
         "activity": "Function quiz (which function for which job?), chart show-and-tell, then Exercise 10 questions and practicals.",
         "outcome": "Students can answer Exercise 10 and demo a chart.", "figures": []},
    ],
    "unit-11": [
        {"period": "Period 1", "topic": "Starting PowerPoint + text boxes",
         "activity": "Lab: open PowerPoint both ways; pupils add a title box, resize, move, recolor and delete it.",
         "outcome": "Students can start PowerPoint and control text boxes.", "figures": []},
        {"period": "Period 2", "topic": "Slides, themes, pictures, shapes, charts",
         "activity": "Build a 3-slide deck: new slide, duplicated slide, theme, one picture, one shape; insert and edit a small chart.",
         "outcome": "Students can build multi-slide content with objects.", "figures": []},
        {"period": "Period 3", "topic": "Transitions, animations, slide show",
         "activity": "Add a transition with sound and speed, animate one object, preview, then run the show both ways.",
         "outcome": "Students can animate and present a slide show.", "figures": []},
        {"period": "Period 4", "topic": "Summary + Exercise 11",
         "activity": "Mini-presentations in groups (2 minutes each), then Exercise 11 questions and practicals.",
         "outcome": "Students can present a deck and answer Exercise 11.", "figures": []},
    ],
    "unit-12": [
        {"period": "Period 1", "topic": "Opening Paint + window parts + features",
         "activity": "Everyone opens Paint; point-and-name tour of menu bar, ribbon, canvas, colour picker, shapes.",
         "outcome": "Students can open Paint and name its parts and features.", "figures": []},
        {"period": "Period 2", "topic": "Drawing: lines, fills, eraser, brush, text",
         "activity": "Draw-a-house task using line, fill, brush and text tools; fix mistakes with the eraser.",
         "outcome": "Students can draw, colour and label a picture.", "figures": []},
        {"period": "Period 3", "topic": "Editing: select, copy, move, resize, crop, rotate, view",
         "activity": "Edit-the-house task: copy a window, move the door, resize, crop, rotate, then zoom and full-screen to check.",
         "outcome": "Students can edit selections and use view tools.", "figures": []},
        {"period": "Period 4", "topic": "Saving, exiting + Summary + Exercise 12",
         "activity": "Save work as JPEG and PNG; compare sizes; exit properly; then Exercise 12 questions and practicals.",
         "outcome": "Students can save, exit and answer Exercise 12.", "figures": []},
    ],
    "unit-13": [
        {"period": "Period 1", "topic": "Introduction + pros and cons",
         "activity": "Hunt for multimedia in the classroom (textbook pictures, speaker, projector); vote advantages vs disadvantages.",
         "outcome": "Students can define multimedia and weigh its pros and cons.", "figures": []},
        {"period": "Period 2", "topic": "Five elements + application areas",
         "activity": "Element match-up: pupils label examples (song, cartoon, photo…) with elements, then map five sectors.",
         "outcome": "Students can explain the five elements and five sectors.", "figures": []},
        {"period": "Period 3", "topic": "Summary + Exercise 13",
         "activity": "Plan-a-mini-project: design a 1-minute multimedia lesson; then Exercise 13 questions.",
         "outcome": "Students can plan multimedia use and answer Exercise 13.", "figures": []},
    ],
    "unit-14": [
        {"period": "Period 1", "topic": "E-commerce, M-commerce, online payment",
         "activity": "Walk through ordering on a Nepali site (demo); pupils list what a wallet/card must do at each step.",
         "outcome": "Students can explain e-commerce, M-commerce and online payment.", "figures": []},
        {"period": "Period 2", "topic": "Cloud, AI, VR",
         "activity": "Save-and-open demo across two machines (cloud idea); pupils name one AI and one VR example each.",
         "outcome": "Students can explain cloud computing, AI and VR with examples.", "figures": []},
        {"period": "Period 3", "topic": "Mobile computing, IoT, smart cities",
         "activity": "Design-a-smart-room task: which devices connect, what do they sense, what do they control?",
         "outcome": "Students can explain mobile computing, IoT and smart cities.", "figures": []},
        {"period": "Period 4", "topic": "Summary + Exercise 14",
         "activity": "Technology timeline quiz, then Exercise 14 questions and full forms.",
         "outcome": "Students can answer Exercise 14 on contemporary technologies.", "figures": []},
    ],
    "unit-15": [
        {"period": "Period 1", "topic": "Language levels + QBASIC intro",
         "activity": "Rank languages machine → assembly → high-level; open QBASIC together and run PRINT “HELLO”.",
         "outcome": "Students can classify languages and open and run QBASIC.", "figures": []},
        {"period": "Period 2", "topic": "Elements: character set → constants",
         "activity": "Board drill: sort names into numeric vs string variables; declare each implicitly, then with DIM.",
         "outcome": "Students can use QBASIC variables, constants and declarations.", "figures": []},
        {"period": "Period 3", "topic": "Operators, expressions, operands",
         "activity": "Evaluate expressions step by step (hierarchy!); pupils predict output before running.",
         "outcome": "Students can use all four operator types with correct order.", "figures": []},
        {"period": "Period 4", "topic": "Statements + example programs",
         "activity": "Type, run and explain all four example programs; pupils modify one (new numbers, new text).",
         "outcome": "Students can write and run short QBASIC programs.", "figures": []},
        {"period": "Period 5", "topic": "Summary + Exercise 15",
         "activity": "Trace-the-output contest with Exercise 15 programs, then remaining questions.",
         "outcome": "Students can trace and answer Exercise 15.", "figures": []},
    ],
}

# ---------------------------------------------------------------------------
# 11. Fresh overview diagrams (the old inline SVGs had misplaced labels).
# {unit_id: (title, svg)}. Injected as a `diagram` block at the end of the
# first section; also replaces the legacy top-level `diagrams` entry.
# ---------------------------------------------------------------------------
def _svg(body, label, h=150):
    return ("<svg viewBox='0 0 400 %d' xmlns='http://www.w3.org/2000/svg' role='img' "
            "aria-label='%s'>" % (h, label)) + body + "</svg>"


T = ("<text x='{x}' y='{y}' text-anchor='middle' fill='{f}' font-size='{s}' "
     "font-family='sans-serif'>{t}</text>")
B = ("<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='9' fill='{f}'/>")
A = ("<line x1='{x1}' y1='{y}' x2='{x2}' y2='{y}' stroke='#0f172a' stroke-width='2'/>"
     "<polygon points='{x2},{y} {x2m}, {ym} {x2m}, {yp}' fill='#0f172a'/>".replace(" ", ""))


def _arrow(x1, x2, y):
    return A.format(x1=x1, x2=x2, y=y, x2m=x2 - 9, ym=y - 5, yp=y + 5)


def _box(x, y, w, h, fill, lines, fs=12, fg="#fff"):
    s = B.format(x=x, y=y, w=w, h=h, f=fill)
    cx = x + w / 2
    if len(lines) == 1:
        s += T.format(x=cx, y=y + h / 2 + 5, f=fg, s=fs, t=lines[0])
    else:
        step = 15
        y0 = y + h / 2 - (len(lines) - 1) * step / 2 + 5
        for i, ln in enumerate(lines):
            s += T.format(x=cx, y=y0 + i * step, f=fg, s=fs, t=ln)
    return s


_INK, _AMB, _EME, _SKY, _VIO = "#0f172a", "#f59e0b", "#059669", "#0ea5e9", "#7c3aed"

DIAGRAMS = {}

_body = (_box(8, 50, 112, 48, _AMB, ["Input"])
         + _arrow(122, 142, 74)
         + _box(144, 50, 112, 48, _EME, ["Process"])
         + _arrow(258, 278, 74)
         + _box(280, 50, 112, 48, _SKY, ["Output"])
         + T.format(x=200, y=128, f="#64748b", s=11,
                    t="Data in → information out"))
DIAGRAMS["unit-1"] = ("Basic Computer Process", _svg(_body, "Basic Computer Process diagram"))

_body = (_box(8, 30, 84, 44, _AMB, ["Input"])
         + _arrow(94, 110, 52)
         + _box(112, 30, 132, 44, _INK, ["CPU: ALU · CU"])
         + _arrow(246, 262, 52)
         + _box(264, 30, 128, 44, _SKY, ["Output"])
         + ("<line x1='178' y1='74' x2='178' y2='92' stroke='#0f172a' stroke-width='2'/>"
            "<polygon points='178,100 173,91 183,91' fill='#0f172a'/>")
         + _box(112, 100, 132, 40, _VIO, ["Memory"])
         + T.format(x=200, y=160, f="#64748b", s=11,
                    t="Input → CPU → Output, with memory"))
DIAGRAMS["unit-2"] = ("Computer Hardware Architecture",
                      _svg(_body, "Computer Hardware Architecture diagram", 172))

_body = (_box(8, 26, 184, 74, _SKY, ["Primary memory", "RAM · ROM · Cache"], 11)
         + _box(208, 26, 184, 74, _EME, ["Secondary memory", "HDD · CD · DVD · SSD"], 11)
         + T.format(x=200, y=128, f="#64748b", s=11,
                    t="Primary = working memory · Secondary = permanent storage"))
DIAGRAMS["unit-3"] = ("Memory Types Comparison", _svg(_body, "Memory Types Comparison diagram"))

_body = (_box(130, 14, 140, 40, _INK, ["Software"])
         + ("<line x1='200' y1='54' x2='200' y2='70' stroke='#0f172a' stroke-width='2'/>"
            "<line x1='110' y1='70' x2='290' y2='70' stroke='#0f172a' stroke-width='2'/>"
            "<line x1='110' y1='70' x2='110' y2='84' stroke='#0f172a' stroke-width='2'/>"
            "<line x1='290' y1='70' x2='290' y2='84' stroke='#0f172a' stroke-width='2'/>")
         + _box(30, 86, 160, 44, _AMB, ["System software"], 11)
         + _box(210, 86, 160, 44, _EME, ["Application software"], 11))
DIAGRAMS["unit-4"] = ("Software Classification", _svg(_body, "Software Classification diagram"))

_body = (_box(8, 50, 112, 48, _AMB, ["User"])
         + _arrow(122, 142, 74)
         + _box(144, 50, 112, 48, _INK, ["Operating", "System"], 11)
         + _arrow(258, 278, 74)
         + _box(280, 50, 112, 48, _SKY, ["Hardware"])
         + T.format(x=200, y=128, f="#64748b", s=11,
                    t="The OS manages memory · files · programs · security"))
DIAGRAMS["unit-5"] = ("OS Functions", _svg(_body, "Operating System Functions diagram"))

_body = (_box(8, 52, 120, 48, _INK, ["ICT"])
         + ("<line x1='128' y1='76' x2='150' y2='34' stroke='#0f172a' stroke-width='2'/>"
            "<line x1='128' y1='76' x2='150' y2='62' stroke='#0f172a' stroke-width='2'/>"
            "<line x1='128' y1='76' x2='150' y2='90' stroke='#0f172a' stroke-width='2'/>"
            "<line x1='128' y1='76' x2='150' y2='118' stroke='#0f172a' stroke-width='2'/>")
         + _box(152, 14, 240, 28, _AMB, ["Education"], 11)
         + _box(152, 48, 240, 28, _EME, ["Banking · Business"], 11)
         + _box(152, 82, 240, 28, _SKY, ["Communication"], 11)
         + _box(152, 116, 240, 28, _VIO, ["Entertainment"], 11))
DIAGRAMS["unit-6"] = ("ICT Applications", _svg(_body, "ICT Applications diagram", 158))

_body = (_box(6, 50, 86, 44, _AMB, ["You"], 11)
         + _arrow(94, 106, 72)
         + _box(108, 50, 86, 44, _VIO, ["ISP"], 11)
         + _arrow(196, 208, 72)
         + _box(210, 50, 86, 44, _INK, ["Internet"], 11)
         + _arrow(298, 310, 72)
         + _box(312, 50, 82, 44, _EME, ["Web", "Email"], 11)
         + T.format(x=200, y=126, f="#64748b", s=11,
                    t="ISP connects you to the Internet's services"))
DIAGRAMS["unit-7"] = ("Internet Network Basics", _svg(_body, "Internet Network Basics diagram"))

_body = (_box(8, 20, 120, 40, "#e11d48", ["Virus"], 11)
         + _box(140, 20, 120, 40, "#e11d48", ["Worm"], 11)
         + _box(272, 20, 120, 40, "#e11d48", ["Trojan"], 11)
         + ("<line x1='200' y1='60' x2='200' y2='78' stroke='#0f172a' stroke-width='2'/>"
            "<polygon points='200,86 195,77 205,77' fill='#0f172a'/>")
         + _box(110, 88, 180, 40, _EME, ["Antivirus stops them"], 11))
DIAGRAMS["unit-8"] = ("Malware Types", _svg(_body, "Malware Types diagram"))

_body = (_box(6, 50, 88, 44, _AMB, ["Create"], 11)
         + _arrow(96, 106, 72)
         + _box(108, 50, 88, 44, _SKY, ["Format"], 11)
         + _arrow(198, 208, 72)
         + _box(210, 50, 88, 44, _VIO, ["Save"], 11)
         + _arrow(300, 310, 72)
         + _box(312, 50, 82, 44, _EME, ["Print"], 11))
DIAGRAMS["unit-9"] = ("MS Word Workflow", _svg(_body, "MS Word Workflow diagram", 120))

_body = (_box(8, 44, 112, 48, _AMB, ["Data"])
         + _arrow(122, 142, 68)
         + _box(144, 44, 112, 48, _VIO, ["Formula"])
         + _arrow(258, 278, 68)
         + _box(280, 44, 112, 48, _EME, ["Result"])
         + T.format(x=200, y=122, f="#64748b", s=11,
                    t="Cell = column + row · e.g. B4"))
DIAGRAMS["unit-10"] = ("Excel Basic Structure", _svg(_body, "Excel Basic Structure diagram", 136))

_body = (_box(6, 50, 88, 44, _AMB, ["Slides"], 11)
         + _arrow(96, 106, 72)
         + _box(108, 50, 88, 44, _SKY, ["Design"], 11)
         + _arrow(198, 208, 72)
         + _box(210, 50, 88, 44, _VIO, ["Animate"], 11)
         + _arrow(300, 310, 72)
         + _box(312, 50, 82, 44, _EME, ["Present"], 11))
DIAGRAMS["unit-11"] = ("Presentation Workflow", _svg(_body, "Presentation Workflow diagram", 120))

_body = (_box(6, 50, 88, 44, _AMB, ["Draw"], 11)
         + _arrow(96, 106, 72)
         + _box(108, 50, 88, 44, "#ec4899", ["Colour"], 11)
         + _arrow(198, 208, 72)
         + _box(210, 50, 88, 44, _SKY, ["Edit"], 11)
         + _arrow(300, 310, 72)
         + _box(312, 50, 82, 44, _EME, ["Save"], 11))
DIAGRAMS["unit-12"] = ("Paint Workflow", _svg(_body, "MS Paint Workflow diagram", 120))

_body = (_box(6, 16, 72, 36, _AMB, ["Text"], 10)
         + _box(86, 16, 72, 36, _SKY, ["Image"], 10)
         + _box(166, 16, 72, 36, _VIO, ["Audio"], 10)
         + _box(246, 16, 72, 36, "#ec4899", ["Video"], 10)
         + _box(322, 16, 72, 36, _INK, ["Animate"], 10)
         + ("<line x1='200' y1='52' x2='200' y2='70' stroke='#0f172a' stroke-width='2'/>"
            "<polygon points='200,78 195,69 205,69' fill='#0f172a'/>")
         + _box(120, 80, 160, 42, _EME, ["Multimedia"], 12))
DIAGRAMS["unit-13"] = ("Multimedia Components", _svg(_body, "Multimedia Components diagram"))

_body = (_box(8, 52, 120, 48, _INK, ["Today's", "Technology"], 11)
         + ("<line x1='128' y1='76' x2='150' y2='40' stroke='#0f172a' stroke-width='2'/>"
            "<line x1='128' y1='76' x2='150' y2='76' stroke='#0f172a' stroke-width='2'/>"
            "<line x1='128' y1='76' x2='150' y2='112' stroke='#0f172a' stroke-width='2'/>")
         + _box(152, 20, 240, 32, _VIO, ["AI · Cloud"], 11)
         + _box(152, 60, 240, 32, _SKY, ["IoT · Smart cities"], 11)
         + _box(152, 100, 240, 32, _EME, ["Mobile · VR · E-commerce"], 11))
DIAGRAMS["unit-14"] = ("Contemporary Technologies",
                       _svg(_body, "Contemporary Technologies diagram"))

_body = (_box(4, 50, 70, 42, _EME, ["Start"], 10)
         + _arrow(76, 84, 71)
         + _box(86, 50, 70, 42, _AMB, ["Input"], 10)
         + _arrow(158, 166, 71)
         + _box(168, 50, 74, 42, _SKY, ["Process"], 10)
         + _arrow(244, 252, 71)
         + _box(254, 50, 70, 42, _VIO, ["Output"], 10)
         + _arrow(326, 334, 71)
         + _box(336, 50, 60, 42, _INK, ["Stop"], 10))
DIAGRAMS["unit-15"] = ("Program Flow", _svg(_body, "Program Flow diagram", 118))
