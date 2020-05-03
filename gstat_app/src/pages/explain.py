import streamlit as st

def print_bdi(text):
    return f"""<div><bdi>{text}</bdi><div>"""

def write():
    st.markdown("<style> div {text-align: left} h2{text-align: left}</style>",
        unsafe_allow_html=True)


    # st.markdown(
    #     """
    #     <h1 style='text-align: center'>הערכת הסבירות לגל שני והיקפו, במגפת הקורונה בישראל, באמצעות מערכת GstatCOVID</h1>
    # <h1 style='text-align: center'>אפרים גולדין </h1>
    # <h1 style='text-align: center'>אפריל 2020</h1>
    #     """,
    #     unsafe_allow_html=True
    # )

    st.markdown(
        """
        <h1 style='text-align: center'><bdi> מערכת GstatCOVID</bdi></h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <html>
    
    <head>
    <meta http-equiv=Content-Type content="text/html; charset=windows-1255">
    <meta name=Generator content="Microsoft Word 15 (filtered)">
    <style>
    <!--
     /* Font Definitions */
     @font-face
        {font-family:Wingdings;
        panose-1:5 0 0 0 0 0 0 0 0 0;}
    @font-face
        {font-family:"Cambria Math";
        panose-1:2 4 5 3 5 4 6 3 2 4;}
    @font-face
        {font-family:Calibri;
        panose-1:2 15 5 2 2 2 4 3 2 4;}
    @font-face
        {font-family:"Calibri Light";
        panose-1:2 15 3 2 2 2 4 3 2 4;}
    @font-face
        {font-family:"Segoe UI";
        panose-1:2 11 5 2 4 2 4 2 2 3;}
     /* Style Definitions */
     p.MsoNormal, li.MsoNormal, div.MsoNormal
        {margin:0in;
        margin-bottom:.0001pt;
        font-size:12.0pt;
        font-family:"Calibri",sans-serif;}
    h1
        {mso-style-link:"Heading 1 Char";
        margin-top:12.0pt;
        margin-right:0in;
        margin-bottom:0in;
        margin-left:.3in;
        margin-bottom:.0001pt;
        text-indent:-.3in;
        page-break-after:avoid;
        font-size:16.0pt;
        font-family:"IBM Plex Sans",sans-serif;
        color:#2F5496;
        font-weight:normal;}
    h2
        {mso-style-link:"Heading 2 Char";
        margin-top:2.0pt;
        margin-right:0in;
        margin-bottom:0in;
        margin-left:.4in;
        margin-bottom:.0001pt;
        text-indent:-.4in;
        page-break-after:avoid;
        font-size:13.0pt;
        font-family:"IBM Plex Sans" ,sans-serif;
        color:#2F5496;
        font-weight:normal;}
    h3
        {mso-style-link:"Heading 3 Char";
        margin-top:2.0pt;
        margin-right:0in;
        margin-bottom:0in;
        margin-left:.5in;
        margin-bottom:.0001pt;
        text-indent:-.5in;
        page-break-after:avoid;
        font-size:12.0pt;
        font-family:"Calibri Light",sans-serif;
        color:#1F3763;
        font-weight:normal;}
    h4
        {mso-style-link:"Heading 4 Char";
        margin-top:2.0pt;
        margin-right:0in;
        margin-bottom:0in;
        margin-left:.6in;
        margin-bottom:.0001pt;
        text-indent:-.6in;
        page-break-after:avoid;
        font-size:12.0pt;
        font-family:"Calibri Light",sans-serif;
        color:#2F5496;
        font-weight:normal;
        font-style:italic;}
    h5
        {mso-style-link:"Heading 5 Char";
        margin-top:2.0pt;
        margin-right:0in;
        margin-bottom:0in;
        margin-left:.7in;
        margin-bottom:.0001pt;
        text-indent:-.7in;
        page-break-after:avoid;
        font-size:12.0pt;
        font-family:"Calibri Light",sans-serif;
        color:#2F5496;
        font-weight:normal;}
    h6
        {mso-style-link:"Heading 6 Char";
        margin-top:2.0pt;
        margin-right:0in;
        margin-bottom:0in;
        margin-left:.8in;
        margin-bottom:.0001pt;
        text-indent:-.8in;
        page-break-after:avoid;
        font-size:12.0pt;
        font-family:"Calibri Light",sans-serif;
        color:#1F3763;
        font-weight:normal;}
    p.MsoHeading7, li.MsoHeading7, div.MsoHeading7
        {mso-style-link:"Heading 7 Char";
        margin-top:2.0pt;
        margin-right:0in;
        margin-bottom:0in;
        margin-left:.9in;
        margin-bottom:.0001pt;
        text-indent:-.9in;
        page-break-after:avoid;
        font-size:12.0pt;
        font-family:"Calibri Light",sans-serif;
        color:#1F3763;
        font-style:italic;}
    p.MsoHeading8, li.MsoHeading8, div.MsoHeading8
        {mso-style-link:"Heading 8 Char";
        margin-top:2.0pt;
        margin-right:0in;
        margin-bottom:0in;
        margin-left:1.0in;
        margin-bottom:.0001pt;
        text-indent:-1.0in;
        page-break-after:avoid;
        font-size:10.5pt;
        font-family:"Calibri Light",sans-serif;
        color:#272727;}
    p.MsoHeading9, li.MsoHeading9, div.MsoHeading9
        {mso-style-link:"Heading 9 Char";
        margin-top:2.0pt;
        margin-right:0in;
        margin-bottom:0in;
        margin-left:1.1in;
        margin-bottom:.0001pt;
        text-indent:-1.1in;
        page-break-after:avoid;
        font-size:10.5pt;
        font-family:"Calibri Light",sans-serif;
        color:#272727;
        font-style:italic;}
    span.Heading1Char
        {mso-style-name:"Heading 1 Char";
        mso-style-link:"Heading 1";
        font-family:"Calibri Light",sans-serif;
        color:#2F5496;}
    span.Heading2Char
        {mso-style-name:"Heading 2 Char";
        mso-style-link:"Heading 2";
        font-family:"Calibri Light",sans-serif;
        color:#2F5496;}
    .MsoChpDefault
        {font-size:12.0pt;
        font-family:"Calibri",sans-serif;}
    @page WordSection1
        {size:595.0pt 842.0pt;
        margin:1.0in 1.0in 1.0in 1.0in;}
    div.WordSection1
        {page:WordSection1;}
     /* List Definitions */
     ol
        {margin-bottom:0in;}
    ul
        {margin-bottom:0in;}
    -->
    </style>
    
    </head>
    
    <body lang=EN-US link="#0563C1" vlink="#954F72">
    
    <div class=WordSection1>
    
    <p class=MsoNormal align=center dir=RTL style='text-align:center;direction:
    rtl;unicode-bidi:embed'><b><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></b></p>
    
    <p class=MsoNormal align=center dir=RTL style='text-align:center;direction:
    rtl;unicode-bidi:embed'><b><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></b></p>
    
    <p class=MsoNormal align=center dir=RTL style='text-align:center;direction:
    rtl;unicode-bidi:embed'><b><span dir=LTR>&nbsp;</span></b></p>

    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:right;
    direction:rtl;unicode-bidi:embed'><b><span dir=LTR>&nbsp;</span></b></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>מערכת
    </span><span dir=LTR>Gstatcovid</span><span dir=RTL></span><span lang=HE
    style='font-family:"Arial",sans-serif'><span dir=RTL></span> פותחה על ידי חברת </span><span
    dir=LTR>GSTAT</span><span dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
    dir=RTL></span>, בתאום עם המשרד למודיעין של ממשלת ישראל. מטרת המערכת היא לספק כלי
    תומך החלטות למשרדי הממשלה האמורים להתמודד עם הלחימה במגפה ובתכנון צעדי היציאה ממנה.
    כמו כן גם לאפשר לציבור הרחב חשיפה למתודולוגיות המידול המתקדמות שבאמצעותן ניתן
    לחזות את התפתחות המגפה. </span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>מערכת
    </span><span dir=LTR>GstatCOVID</span><span dir=RTL></span><span
    style='font-family:"Arial",sans-serif'><span dir=RTL></span> <span lang=HE>שונה
    ממערכות המידע הרבות המציגות דשבורדים של נתוני התפתחות המגפה בכך  שהיא כוללת מעבר
    לדשבורדים גם מודלים סטטיסטיים מתקדמים המאפשרים לחזות את התפתחות המגפה (כמות
    חולים, מונשמים ועוד), מתחילתה ועד לבלימתה. בכך המערכת נותנת כלים רבי עוצמה
    למקבלי ההחלטות המתמודדים עם האי הוודאות הרבה לגבי התפתחות המגפה. </span></span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>התחזיות
    שבלב המערכת מתעדכנות באופן יומי על בסיס המידע העדכני המצטבר מהעולם לגבי תוכניות
    השחרור ועל השפעתן על מקדמי ההדבקה בעולם.  בכך היא מספקת כלי זמן אמת עדכניים למקבלי
    ההחלטות. </span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>פתוח
    המערכת נעשה על ידי צוות של מדעני נתונים  </span><span dir=LTR></span><span
    dir=LTR><span dir=LTR></span>(Data Scientists)</span><span dir=RTL></span><span
    lang=HE style='font-family:"Arial",sans-serif'><span dir=RTL></span> מצטיינים מ-
    </span><span dir=LTR>Gstat</span><span dir=RTL></span><span lang=HE
    style='font-family:"Arial",sans-serif'><span dir=RTL></span> שבצעו את העבודה
    בהתנדבות,</span><span dir=LTR></span><span lang=HE dir=LTR><span dir=LTR></span>
    </span><span lang=HE style='font-family:"Arial",sans-serif'>כשחלקם היו
    בחל&quot;ת בתקופת הפתוח. המערכת פותחה כתרומה של צוות המתנדבים ו- </span><span
    dir=LTR>Gstat</span><span dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
    dir=RTL></span>, למאמץ הלאומי הכולל למלחמה במגפה ולתהליכי היציאה ממנה. </span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>פרופסור
    מיכאל בינסטוק מהאוניברסיטה העברית חבר לצוות ופתח מודל חדשני וייחודי לכימות
    ההשפעה של צעדי המדיניות על היקף התפתחות המגפה. עבודתו שחלקים ממנה מיושמים
    במערכת ושבמסגרתה הוא השתמש להדגמת המתודולוגיה בנתוני ישראל, התפרסמה בימים אלו
    בעיתונות המקצועית (ראה </span><b><a href="https://github.com/gstat-gcloud/covid19-sim/raw/master/Resources/Natural_and_Unnatural_Histories_of_Covid19.pdf"><span dir=LTR style='font-family:"Times New Roman",serif'>Michael
    Beenstock</span></b><span dir=RTL></span><b><span lang=HE style='font-family:
    "Times New Roman",serif'><span dir=RTL></span> &amp; </span></b><b><span
    dir=LTR style='font-family:"Times New Roman",serif'>Xieer Dai</span></b><span
    dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
    dir=RTL></span>).</a></span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>המערכת
    זמינה באינטרנט ופתוחה לכל משתמש שרוצה להשתמש בה ולהבין בצורה מעמיקה את תהליכי ההתפרצות
    והבלימה של מגפת הקורונה בישראל ובעולם, על בסיס מידול מתקדם.</span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>בהמשך
    אנו מדגימים את השימוש במודל  </span><span dir=LTR>GstatCOVID</span><span
    dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
    dir=RTL></span>, לצורך מתן הערכה מבוססת נתונים עדכניים מהעולם לגבי הסבירות
    להתפרצות גל שני, ולגבי היקפו במידה ויתפרץ.</span></p>
    
    <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
    direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>

    </div>
    
    </body>
    
    </html>
    
        """,
    unsafe_allow_html=True
    )

