This project aims to visualize research topics for materials scientists by analyzing thier publications using natural language processing.
This tool takes a collection of XML documents grouped by each researcher and processes them then extracts topic terms.
Topic terms are visualized using word cloud technique.
Based on the extracted terms, similarity can be computed between 2 researchers.

# Usage

To use this tool, please add a folder nameed "Authors_XML" under which each researcher has its own folder that contains publications in XML format.
First run the processXML.py file, then Word_cloud_vis.py file
You will get an "Authors_TXT" folder that contains several subfolders each of which is for a researher and contains extracted texts from the publications.
Additionally, you will get "word_cloud" folder contains the PNG images for the generated wordcloud and the terms with their wights.


# Feedback
dieb.sae@gmail.com


