# Class 6 — figure files needed

The Class 6 pages reference **80 textbook figures** under `public/figures/class6/`.
That folder is gitignored by design (see SETUP.md §7), so a fresh `git clone` does not contain them.
Until they are restored, every figure slot shows a graceful captioned placeholder instead of a broken image.

## How to restore them

1. Take the **setup zip** of the study.companion (it carries all figures).
2. Copy its `public/figures/class6/` folder into this repo at `public/figures/class6/` (same relative path).
3. Rebuild (`npm run build`) — Next.js copies `public/figures/` into `dist/figures/` automatically.
4. Verify: `find dist/figures/class6 -type f | wc -l` should print **80**.

If you deploy from git (Vercel/Netlify/etc.), note the host also clones without these files — either commit the figures (remove the `public/figures/` line from `.gitignore`) or upload them to the host separately. Large-file hosts may prefer Git LFS.

## Required files (80)

### Chapter 1 — Introduction to Computers
- `/figures/class6/characteristics-features-of-computer.jpg` — Characteristics (Features) of Computer (textbook p. 3)
- `/figures/class6/computer-in-education.jpg` — Computer in Education (textbook p. 5)
- `/figures/class6/computer-in-business.jpg` — Computer in Business (textbook p. 5)
- `/figures/class6/computer-in-office.jpg` — Computer in Office (textbook p. 6)
- `/figures/class6/computer-in-communication.jpg` — Computer in Communication (textbook p. 7)
- `/figures/class6/computer-in-bank.jpg` — Computer in Bank (textbook p. 7)

### Chapter 2 — Computer Hardware
- `/figures/class6/computer-hardware-components.jpg` — Computer Hardware Components (textbook p. 11)
- `/figures/class6/mouse.jpg` — Mouse (textbook p. 12)
- `/figures/class6/touchpad.jpg` — Touchpad (textbook p. 13)
- `/figures/class6/joystick-and-its-different-forms.jpg` — Joystick and its Different Forms (textbook p. 13)
- `/figures/class6/touch-screen.jpg` — Touch Screen (textbook p. 14)
- `/figures/class6/central-processing-unit.jpg` — Central Processing Unit (textbook p. 15)
- `/figures/class6/memory-devices.jpg` — Memory Devices (textbook p. 16)
- `/figures/class6/crt-monitor.jpg` — CRT Monitor (textbook p. 18)
- `/figures/class6/lcd-monitor.jpg` — LCD Monitor (textbook p. 18)
- `/figures/class6/led-monitor.jpg` — LED Monitor (textbook p. 19)
- `/figures/class6/printer.jpg` — Printer (textbook p. 19)

### Chapter 3 — Memory Devices
- `/figures/class6/ram.jpg` — RAM (textbook p. 25)
- `/figures/class6/rom.jpg` — ROM (textbook p. 25)
- `/figures/class6/hard-disk.jpg` — Hard Disk (textbook p. 26)
- `/figures/class6/dvd.jpg` — DVD (textbook p. 27)
- `/figures/class6/memory-chip-card.jpg` — Memory Chip/Card (textbook p. 28)
- `/figures/class6/pen-drives.jpg` — Pen Drives (textbook p. 28)
- `/figures/class6/solid-state-drive-ssd.jpg` — Solid State Drive (SSD) (textbook p. 29)

### Chapter 4 — Computer Software
- `/figures/class6/types-of-software.jpg` — Types of Software (textbook p. 33)
- `/figures/class6/application-softwares.jpg` — Application Softwares (textbook p. 34)

### Chapter 5 — Operating System
- `/figures/class6/desktop-of-window-11.jpg` — Desktop of Window 11 (textbook p. 41)
- `/figures/class6/start-menu.jpg` — Start Menu (textbook p. 42)
- `/figures/class6/various-icons-found-in-windows.jpg` — Various Icons Found in Windows (textbook p. 43)
- `/figures/class6/login-screen-of-windows-11.jpg` — Login Screen of Windows 11 (textbook p. 44)
- `/figures/class6/shut-down-dialog-window-to-turn-the-computer-off-sleep-and.jpg` — Shut Down Dialog Window to Turn the Computer Off, Sleep and Restart (textbook p. 44)

### Chapter 6 — Information and Cyber Law
- `/figures/class6/application-areas-of-ict.jpg` — Application Areas of ICT (textbook p. 52)
- `/figures/class6/ict-in-education.jpg` — ICT in Education (textbook p. 52)
- `/figures/class6/ict-in-banking.jpg` — ICT in Banking (textbook p. 53)
- `/figures/class6/ict-in-business.jpg` — ICT in Business (textbook p. 53)
- `/figures/class6/ict-in-communication-and-entertainment.jpg` — ICT in Communication and Entertainment (textbook p. 54)

### Chapter 7 — Internet and Email
- `/figures/class6/world-wide-web.jpg` — World Wide Web (textbook p. 60)
- `/figures/class6/web-browser.jpg` — Web Browser (textbook p. 61)
- `/figures/class6/webpage.jpg` — Webpage (textbook p. 61)
- `/figures/class6/search-engine.jpg` — Search Engine (textbook p. 63)
- `/figures/class6/google.jpg` — Google (textbook p. 63)
- `/figures/class6/email.jpg` — Email (textbook p. 64)

### Chapter 8 — Computer Malware
- `/figures/class6/symptoms-of-malware.jpg` — Symptoms of Malware (textbook p. 71)
- `/figures/class6/antivirus-softwares.jpg` — Antivirus Softwares (textbook p. 72)

### Chapter 9 — Word Processing
- `/figures/class6/save-a-copy-of-a-file-6.jpg` — Save a Copy of a File (textbook p. 78)
- `/figures/class6/save-a-copy-of-a-file-6-8d394.jpg` — Save a Copy of a File (textbook p. 78)
- `/figures/class6/select-text-6.jpg` — Select Text (textbook p. 80)
- `/figures/class6/add-wordart-6.jpg` — Add WordArt (textbook p. 82)
- `/figures/class6/insert-a-picture-from-a-file-6.jpg` — Insert a Picture From a File (textbook p. 85)
- `/figures/class6/inserting-shapes-6.jpg` — Inserting Shapes (textbook p. 86)

### Chapter 10 — Spreadsheet Software
- `/figures/class6/cell-reference-cell-address-6.jpg` — . Cell Reference (Cell Address) (textbook p. 92)
- `/figures/class6/ms-excel-6.jpg` — MS Excel (textbook p. 92)
- `/figures/class6/how-to-open-ms-excel-2016-6.jpg` — How to Open MS Excel 2016? (textbook p. 93)
- `/figures/class6/how-to-open-ms-excel-2016-6-6383c.jpg` — How to Open MS Excel 2016? (textbook p. 93)
- `/figures/class6/formatting-the-data-in-the-worksheet-6.jpg` — Formatting the Data in the Worksheet (textbook p. 94)
- `/figures/class6/borders-6.jpg` — Borders (textbook p. 96)
- `/figures/class6/examples-of-mathematical-calculations-6.jpg` — Examples of Mathematical Calculations (textbook p. 99)
- `/figures/class6/creating-a-chart-6.jpg` — Creating a Chart (textbook p. 100)
- `/figures/class6/creating-a-chart-6-1a831.jpg` — Creating a Chart (textbook p. 100)

### Chapter 11 — Presentation Software
- `/figures/class6/to-start-microsoft-powerpoint-2016-6.jpg` — To Start Microsoft PowerPoint 2016 (textbook p. 107)
- `/figures/class6/to-start-microsoft-powerpoint-2016-6-99f8f.jpg` — To Start Microsoft PowerPoint 2016 (textbook p. 107)
- `/figures/class6/adding-slides-6.jpg` — Adding Slides (textbook p. 109)
- `/figures/class6/themes-6.jpg` — Themes (textbook p. 110)
- `/figures/class6/insert-the-data-and-labels-6.jpg` — . Insert the Data and Labels. (textbook p. 111)
- `/figures/class6/slide-transition-6.jpg` — Slide Transition (textbook p. 112)
- `/figures/class6/slide-show-options-6.jpg` — Slide Show Options (textbook p. 113)

### Chapter 12 — Drawing using MS Paint
- `/figures/class6/components-of-ms-paint-window.jpg` — Components of MS Paint Window (textbook p. 118)
- `/figures/class6/features-of-ms-paint.jpg` — Features of Ms Paint (textbook p. 119)

### Chapter 13 — Multimedia
- `/figures/class6/components-of-multimedia.jpg` — Components of Multimedia (textbook p. 135)
- `/figures/class6/application-areas-of-multimedia.jpg` — Application Areas of Multimedia (textbook p. 137)

### Chapter 14 — Contemporary Technologies
- `/figures/class6/social-media.jpg` — Social Media (textbook p. 141)
- `/figures/class6/e-commerce.jpg` — E-commerce (textbook p. 141)
- `/figures/class6/m-commerce.jpg` — M-commerce (textbook p. 142)
- `/figures/class6/online-payment.jpg` — Online Payment (textbook p. 142)
- `/figures/class6/cloud-computing.jpg` — Cloud Computing (textbook p. 143)
- `/figures/class6/artificial-intelligence.jpg` — Artificial Intelligence (textbook p. 144)
- `/figures/class6/virtual-reality.jpg` — Virtual Reality (textbook p. 144)
- `/figures/class6/mobile-computing.jpg` — Mobile Computing (textbook p. 145)
- `/figures/class6/lot.jpg` — loT (textbook p. 146)

### Chapter 15 — Computer Programming
- `/figures/class6/elements-of-qbasic-programming.jpg` — Elements of QBASIC Programming (textbook p. 153)
