# Tab 1

- A bunch of procedures to organize the work in a startup  
- Standardize workflows  
- Convert our documentation into book chapters  
- Put everything into a book  
- Topics  
  - On-boarding  
  - Hiring  
  - Interviewing people  
  - Creating an open source arm  
  - Roles  
    - InfraMeister  
  - CI/CD  
  - Infra  
  - How to organize research  
  - How to organize your time / productivity

## **Resources**

Next from I-Corps: [https://drive.google.com/drive/folders/1jsP3sykxbNauttCsHD7mxoMMZb4cDKiA](https://drive.google.com/drive/folders/1jsP3sykxbNauttCsHD7mxoMMZb4cDKiA)

[https://www.startupguide.umd.edu/](https://www.startupguide.umd.edu/)

MIT 15.390 New Enterprises, Spring 2013  
https://ocw.mit.edu/courses/15-390-new-enterprises-spring-2013  
[https://www.youtube.com/playlist?list=PLUl4u3cNGP63CLq-GxVm4VSr-0iKAS-07](https://www.youtube.com/playlist?list=PLUl4u3cNGP63CLq-GxVm4VSr-0iKAS-07)

[https://em-execed.stanford.edu/launching-a-startup](https://em-execed.stanford.edu/launching-a-startup)

https://www.coursicle.com/umd/courses/BUSO/712/

### **~~Business model~~**

~~/Users/saggese/src/notes1/notes/IN\_PROGRESS.book.work.2011.Osterwalder.Business\_model\_generation.txt~~  
~~/Users/saggese/src/notes1/notes/IN\_PROGRESS.book.work.2020.Blank.The\_Startup\_Owner\_Manual.txt~~  
~~/Users/saggese/src/notes1/notes/IN\_PROGRESS[.course.cs](http://.course.cs).entrepreneurship\_in\_web3.Berkeley.txt~~  
~~Lean startup~~  
~~/Users/saggese/src/notes1/notes/IN\_PROGRESS.tutorial.2023.I\_Corps.txt~~  
~~/Users/saggese/src/notes1/notes/IN\_PROGRESS.tutorial.2023.National\_I\_Corps.txt~~

### **~~Executive team organization~~**

~~notes/work.The\_first\_time\_manager.2012.txt~~  
~~notes/IN\_PROGRESS.book.2017.Fournier.The\_manager\_s\_Path.txt~~  
~~notes/tools.An\_elegant\_puzzle.Larson.2019.txt~~

### **~~Tech team organization~~**

~~/Users/saggese/src/notes1/notes/IN\_PROGRESS.cs.The\_Scrum\_field\_guide.Lacey.2012.txt~~  
~~tools.zenhub.txt~~

### **Sales**

notes/IN\_PROGRESS.book.2022.Mastering\_technical\_sales.Care.txt

### **Fundraising**

notes/IN\_PROGRESS.book.startup.The\_fundraising\_strategy\_playbook.2021.Sheikh.txt

### **Tool org**

~~/Users/saggese/src/notes1/notes/IN\_PROGRESS.startup.Come\_up\_for\_air.Sonnenberg.2023.txt~~

### **Misc**

notes/work.Rework.Basecamp.2010.txt

IN\_PROGRESS.book.2014.Talking\_to\_humans.Constable.txt  
IN\_PROGRESS.book.2017.Fournier.The\_manager\_s\_Path.txt

IN\_PROGRESS.book.sales.The\_JOLT\_effect.Dixon.2022.txt  
IN\_PROGRESS.book.startup.The\_fundraising\_strategy\_playbook.2021.Sheikh.txt  
IN\_PROGRESS.book.work.2011.Osterwalder.Business\_model\_generation.txt  
IN\_PROGRESS.book.work.2020.Blank.The\_Startup\_Owner\_Manual.txt

IN\_PROGRESS.startup.Come\_up\_for\_air.Sonnenberg.2023.txt

self.Getting\_things\_done.Allen.2001.txt

tools.An\_elegant\_puzzle.Larson.2019.txt

# Issues

### **ISSUE: Convert a markdown book into slides**

- The input is a markdown file  
- Extract the headers

/Applications/calibre.app/Contents/MacOS/ebook-convert \~/Downloads/Wickman\\,\\ Gino\\ \-\\ What\\ the\\ Heck\\ Is\\ EOS\_\\ \\(BenBella\\ Books\\,\\ Inc.\\)\\ \-\\ libgen.li.epub ./oeb

pandoc oeb/content.opf \-f html \-t gfm \-o [output.md](http://output.md)

pandoc oeb/OEBPS/Title.html        oeb/OEBPS/Halftitle.html        oeb/OEBPS/Copyright.html        oeb/OEBPS/Dedication.html        oeb/OEBPS/Contents.html        oeb/OEBPS/Introduction.html        oeb/OEBPS/Chapter\*.html        oeb/OEBPS/Appendix\*.html        oeb/OEBPS/Acknowledgments.html        oeb/OEBPS/Author.html        \-f html \-t gfm \-o [output.md](http://output.md)

#### Approach 2

/Applications/calibre.app/Contents/MacOS/ebook-convert \~/Downloads/Wickman\\,\\ Gino\\ \-\\ What\\ the\\ Heck\\ Is\\ EOS\_\\ \\(BenBella\\ Books\\,\\ Inc.\\)\\ \-\\ libgen.li.epub output.docx

convert\_docx\_to\_markdown.py \--docx\_file output.docx \--md\_file [output2.md](http://output2.md)

rename /app \-\> . for the figures

open\_md\_in\_browser.sh [output2.md](http://output2.md)

extract\_headers\_from\_markdown.py \-i [output2.md](http://output2.md)

 extract\_headers\_from\_markdown.py \-i output2.md \--mode cfile

### **ISSUE: Extract notes**

Prompt: 

Here are rules to summarize a text into a set of markdown bullets.

\<RULES\>  
/Users/saggese/src/tutorials1/guidelines\_for\_notes.txt  
\</RULES\>

\- Summarize the text below using the RULES and output only markdown code

\<TEXT\>  
\</TEXT\>

### **ISSUE: Workflow to merge the docs**

- Read all the slides in a file  
  - There should be a function for doing that (extract\_slides\_from\_markdown)  
- Make sure that all the slides have a title  
  - If not create one from the content  
- Each slide has a path in terms of headers  
  - (header1, header2, slide title, text)  
- Read all the topics from all the files  
  - ls \-1 chap\*.txt  
- Map each slide on one of the topics using LLM in one shot or in multiple shots  
  - file, slide, line \-\> file, header  
- Create a cfile list of all the slides that don't correspond to a topic  
  - So we can quickly review them  
  - Propose new topics in the file that might cover the slides  
- If a map is approved, copy all the slides to the right place  
  - Add a reference to the original file

### **Process each slide**

- Apply a prompt (e.g., improve, reduce) each slide of a file

### **Scan the slides looking for an opportunity to create a visual**

### **Redistribute content**

Step 1

In this directory there are several files TOPIC\_FILES that you can find with  
\> ls \-1 chap\*.txt

For example  
chap00.Introduction.txt  
chap01.Introduction\_to\_Startups.txt  
chap02.Problem\_Discovery\_and\_Opportunity\_Identification.txt  
chap03.Ideation\_and\_Value\_Proposition\_Design.txt  
chap04.Customer\_Discovery\_and\_Validation.txt  
chap05.Business\_Models\_and\_Product-Market\_Fit.txt

Every file is a markdown with various topics inside separated by headers

Step 2  
Read the file \<FILE1\> /Users/saggese/src/notes1/notes/IN\_PROGRESS.book.work.2011.Osterwalder.Business\_model\_generation.txt

This is a markdown file with headers  
Each paragraph PARAGRAPH1 starts with a star and a title \<TITLE\> and has bullet points,  
for instance:  
\`\`\`  
\* Web3 startups  
\- Attention to web3 exploded in recent years  
\- Better incentive models and control to users  
...  
\`\`\`

Step 3

Distribute the content from the first 10 paragraphs of FILE1 across the different topics  
described in the files TOPIC\_FILES

Each paragraph from FILE1 should be copied without any change into the right place  
in one of the file TOPIC\_FILES, based on the relevance of its topic

Each paragraph from FILE1 should be used only once

Paragraphs that don't match any of the topics should be ignored

Before adding the new PARAGRAPH add a note like  
// From \<FILE1\>

Do not output comment or explanations