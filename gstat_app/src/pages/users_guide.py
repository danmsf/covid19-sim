import streamlit as st

def write():
    st.markdown(
        """
        
        <h1 dir=RTL style='margin-top:12.0pt;margin-right:.3in;margin-bottom:0in;
        margin-left:0in;margin-bottom:.0001pt;text-align:right;direction:rtl;
        unicode-bidi:embed'>
        </span></span><span dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'>בעיית
        חיזוי הגל השני</span></h1>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><b><span dir=LTR>&nbsp;</span></b></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>מדינות
        רבות בעולם נמצאות בתהליכי יציאה מאמצעי המדיניות הנוקשים שננקטו לבלימת התפשטות
        מגפת הקורונה ולמניעת הצפת מערכות הבריאות בעולם בביקוש למכשירי הנשמה מעבר להיצע הקיים.
        אמצעי  המדיניות העיקריים שננקטו במינונים שונים ובשלבים שונים של ההתפרצות היו בין
        השאר איסור התקהלויות, סגירת חנויות ומרכזי מסחר, סגירת שדות תעופה ומעברים בין
        מדינות, סגירת מוסדות לימוד, הורדת היקף העבודה ברמות שונות, הסגרים, עוצר מלא
        ועוד. </span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>מדד
        להתפתחות חומרת הצעדים, המוצג במערכת, הינו </span><span dir=LTR>Oxford
        stringency Index</span><span dir=RTL></span><span lang=HE style='font-family:
        "Arial",sans-serif'><span dir=RTL></span>. המדד משקלל את צעדי המדיניות בכל
        מדינה ובכל יום במספר שבין 0 ל-100, כאשר 0 הוא מצב של אי נקיטת צעדים כלל ו-100
        הינו מצב של סגר מלא. המדד מאפשר לחקור את הקשרים בין מועדי הצעדים ועוצמתם
        במדינות שונות בעולם לבין ההצלחה בבלימת התפשטות המגפה.</span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>כיום
        נעשים מחקרים רבים למדידת הקשר בין רמת הצעדים שננקטו לבין ההשפעה על קצב התפשטות
        המגפה. הניתוח נעשה בדרך כלל על ידי בדיקת ההשפעה הדינמית של צעדי המדיניות על
        הורדת מדד </span><span dir=LTR></span><span dir=LTR><span dir=LTR></span>,</span><span
        dir=LTR>R</span><span dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> או </span><span dir=LTR>R</span><span dir=LTR>0</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span>. </span><span dir=LTR>R</span><span dir=RTL></span><span
        lang=HE style='font-family:"Arial",sans-serif'><span dir=RTL></span> או  </span><span
        dir=LTR>R0</span><span dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> הינו מספר האנשים שמדביק כל חולה, בשלב המחלה שבו הוא מדבק. ידיעה
        וחיזוי של </span><span dir=LTR></span><span dir=LTR><span dir=LTR></span>,R</span><span
        dir=RTL></span><span style='font-family:"Arial",sans-serif'><span dir=RTL></span>
        <span lang=HE>ותחת מספר הנחות נוספות, מאפשרת  לחזות את רוב המשתנים הקשורים
        להתפתחות המגפה, כמו מספר החולים החדשים, מספר החולים הקשים, מספר המתים ועוד.</span></span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:right;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>לו
        היינו צופים בכל החולים שנדבקו, אמידת </span><span dir=LTR>R</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> וההשפעה של אמצעי המדיניות על שיעורי הירידה בו בשלבי הבלימה,
        הייתה יחסית פשוטה, שכן מדובר בתהליך גאומטרי פשוט. אולם בפועל אמידת </span><span
        dir=LTR>R</span><span dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> הינה מאתגרת שכן אנו יודעים כיום שרבים מבין המדבקים הינם חסרי
        סימפטומים ולא מדווחים כחולים. בנוסף ישנן בעיות של דיווחים לא מדויקים, ועוד. רוב
        הגישות המקובלות לאמידה מבוססות לכן על הנחות לגבי הגדלים הבלתי נצפים ומתבססות על
        המודלים האפידמיולוגיים ממשפח </span><span dir=LTR><a href="https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology" target="_blank">SIR</a></span><span dir=RTL></span><span
        lang=HE style='font-family:"Arial",sans-serif'><span dir=RTL></span> ,
        הנאמדים בדרך כלל באמצעות מודל </span><span dir=LTR>MCMC</span><span dir=RTL></span><span
        style='font-family:"Arial",sans-serif'><span dir=RTL></span> <span lang=HE>שכולל
        בתוכו הנחות אפריוריות על הגדלים הלא ידועים (</span></span><span dir=LTR><a href="https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo" target="_blank">Monte
        Carlo Markov Chains models</a></span><span dir=RTL></span><span lang=HE
        style='font-family:"Arial",sans-serif'><span dir=RTL></span>). </span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'><br
        clear=all>
        </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><b><span lang=HE style='font-family:"Times New Roman",serif'>&nbsp;</span></b></p>
        
        <p class=MsoNormal align=center dir=RTL style='text-align:center;direction:
        rtl;unicode-bidi:embed'><b><span dir=LTR style='font-family:"Times New Roman",serif'>&nbsp;</span></b></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>במאמר
        שהתפרסם על ידי (</span><a href="https://cepr.org/sites/default/files/news/CovidEconomics10.pdf" target="_blank"><b><span dir=LTR style='font-family:"Times New Roman",serif'>Michael
        Beenstock</span></b><span dir=RTL></span><b><span lang=HE style='font-family:
        "Times New Roman",serif'><span dir=RTL></span> &amp; </span></b><b><span
        dir=LTR style='font-family:"Times New Roman",serif'>Xieer Dai</span></b></a><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span>) מוצגת הדרך שבה אנו אמדנו את </span><span dir=LTR>R</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> במודל שלנו, המבוססת על מודל </span><span dir=LTR>OLG</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> (</span><span dir=LTR>Over Lapping Generations</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span>). במאמר </span><span dir=LTR></span><span dir=LTR><span
        dir=LTR></span></span><span
        dir=RTL></span><span style='font-family:"Arial",sans-serif'><span dir=RTL></span>
        <span lang=HE> דיון ביתרונות והחסרונות של גישת </span></span><span dir=LTR>OLG</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> לעומת גישת </span><span dir=LTR>MCMC</span><span dir=RTL></span><span
        lang=HE style='font-family:"Arial",sans-serif'><span dir=RTL></span> מבוססת </span><span
        dir=LTR>SIR</span><span dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span>.</span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>בהינתן
        אומדנים של </span><span dir=LTR>R</span><span dir=RTL></span><span lang=HE
        style='font-family:"Arial",sans-serif'><span dir=RTL></span> במדינות שונות ניתן
        לבחון באמצעות ניתוחי חתכים</span><span dir=LTR></span><span lang=HE dir=LTR><span
        dir=LTR></span> </span><span lang=HE style='font-family:"Arial",sans-serif'>לאורך
        זמן (</span><span dir=LTR>Panel data analysis, Longitudinal Data analysis…</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span>), את האפקטיביות של אמצעי המדיניות השונים על בסיס נתונים
        השוואתיים בין מדינות שנקטו צעדי מדיניות שונים בנקודות זמן שונות. דוגמא לעבודה
        כזו היא</span><span dir=LTR></span><span dir=LTR><span dir=LTR></span>:</span><span
        dir=RTL></span><span style='font-family:"Arial",sans-serif'><span dir=RTL></span>
        </span></p>
        
        <p class=MsoNormal><span style='font-family:"Times New Roman",serif'>Xiaohui
        Chen<span dir=RTL></span><span dir=RTL><span dir=RTL></span> </span><span
        dir=LTR></span><span dir=LTR></span> and Ziyi Qiu<span dir=RTL></span><span
        lang=HE dir=RTL><span dir=RTL></span>&quot; </span><i><a href="https://cepr.org/sites/default/files/news/CovidEconomics7.pdf" target="_blank">Scenario analysis of non&#8209;pharmaceutical
        interventions on global Covid-19 transmissions</a></i><span dir=RTL></span><span
        lang=HE dir=RTL><span dir=RTL></span> &quot;  </span></span><span
        style='font-size:9.0pt;font-family:"Times New Roman",serif'>COVID ECONOMICS</span><span
        style='font-size:9.0pt;font-family:"Times New Roman",serif'>, </span><span
        style='font-size:9.0pt;font-family:"Times New Roman",serif'>ISSUE 7 20 APRIL
        2020</span></p>
        
        <p class=MsoNormal><span style='font-family:"Times New Roman",serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>בעת
        כתיבת דברים אלו (סוף אפריל 2020) שיאי המגפה ברוב מדינות העולם וישראל כבר
        מאחורינו ולכן השאלה העיקרית שעל הפרק הינה חיזוי ההשפעה של אמצעי השחרור על
        העלייה הצפויה ב- </span><span dir=LTR>R</span><span dir=RTL></span><span
        style='font-family:"Arial",sans-serif'><span dir=RTL></span> <span lang=HE>ועל
        הסבירות להתפרצות גל שני. אם ההשפעה סימטרית, כלומר ההשפעה של אמצעי המדיניות על
        הירידה במקדם ההדבקה בעת ההתפרצות היא באותה עוצמה, אולם בכיוון ההפוך בעת תהליך
        השחרור, ניתן להשתמש במקדמים שנאמדו לתהליך ההתפרצות.</span></span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>אולם
        לא היא. הנתונים מסין, שנמצאת בשלבי שחרור מתקדמים ביותר, יחסית לרוב מדינות
        העולם, מלמדים שלמרות שחלק גדול מצעדי המדיניות שננקטו בזמן ההתפרצות שוחררו מזמן,
        אין כמעט תופעות של התפרצות מחודשת, או מה שנקרא גל שני, אם כי יש במספר פרובינציות
        עלייה בשיעורי ההדבקה. גם במדינות כמו סינגפור והונג קונג, שבהן נרשמה התפרצות
        שנייה, היא נבלמה מהר מאוד ולא הובילה לעלייה משמעותית במקדם ההדבקה. </span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>ההסבר
        לכך הוא כפי הנראה שכאשר משחררים את אמצעי המדיניות המגבילים, איננו חוזרים לאותו
        עולם. הציבור ממשיך להגן על עצמו ומתרחק מתוך חשש מהידבקות בעת שהייתו במרחב הציבורי,
        הציבור הולך עם מסכות, סביבת העבודה ואמצעי הבקרה בכניסה למקומות עבודה ולחנויות
        משתנים ועוד.  </span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='margin-right:10.0pt;text-align:justify;
        direction:rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Arial",sans-serif'>מאחר
        ואין עדיין מספיק דוגמאות ממדינות שונות בעולם על ההשפעה על צעדי שחרור שונים על
        העלייה ב- </span><span dir=LTR>R</span><span dir=RTL></span><span lang=HE
        style='font-family:"Arial",sans-serif'><span dir=RTL></span>, נקטנו לצורך חיזוי
        הסבירות של הגל השני בישראל וחיזוי היקפו, בגישה השוואתית המנסה למצות את המירב
        מהמידע הידוע ממדינות שבהם תהליך השחרור מתקדם יותר במידה זו או אחרת מאשר בישראל.
        </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><b><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></b></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <h1 dir=RTL style='margin-top:12.0pt;margin-right:.3in;margin-bottom:0in;
        margin-left:0in;margin-bottom:.0001pt;text-align:right;direction:rtl;
        unicode-bidi:embed'><span dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'>שימוש
        במערכת </span><span dir=LTR style='font-family:"Arial",sans-serif'>GstatCOVID</span><span
        dir=RTL></span><span style='font-family:"Arial",sans-serif'><span dir=RTL></span>
        <span lang=HE> להערכת הסבירות וההיקף של התפרצות גל שני בישראל </span></span></h1>
        
        <h2 dir=RTL style='margin-top:2.0pt;margin-right:.4in;margin-bottom:0in;
        margin-left:0in;margin-bottom:.0001pt;text-align:right;direction:rtl;
        unicode-bidi:embed'><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'>השוואת
        התנהגות של מקדם ההדבקה </span><span dir=LTR style='font-family:"Arial",sans-serif'>R</span><span
        dir=RTL></span><span style='font-family:"Arial",sans-serif'><span dir=RTL></span>
         <span lang=HE>לאורך תקופת המגפה, במדינות שונות בעולם</span></span></h2>
        
        <h2 dir=RTL style='margin-left:0in;text-align:right;text-indent:0in;direction:
        rtl;unicode-bidi:embed'><span lang=HE style='font-family:"Times New Roman",serif'>&nbsp;</span></h2>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>מערכת </span><span
        dir=LTR>GstatCOVID</span><span dir=RTL></span><span lang=HE style='font-family:
        "Arial",sans-serif'><span dir=RTL></span> כוללת יכולות מובנות לחשב את מקדמי
        ההדבקה במדינות שונות בעולם ולהשוות בינהן. </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span dir=LTR><img width=700 height=300 id="Picture 2"
        src="https://github.com/gstat-gcloud/covid19-sim/raw/master/gstat_app/src/assets/images/image002.jpg"
        alt="A screenshot of a cell phone&#10;&#10;Description automatically generated"></span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>בחירה ב- </span><span
        dir=LTR>Compare Countries Data</span><span dir=RTL></span><span lang=HE
        style='font-family:"Arial",sans-serif'><span dir=RTL></span> מאפשרת לבחור
        מדינות להשוואה. ציר הזמן נמדד או בזמן קלנדרי או בזמן קורונה. ברירת המחדל הינה
        זמן קורונה המוגדר כמספר הימים מאז שנרשמו לראשונה כמות מקרים מאומתים הגדולה או
        שווה לפרמטר שנקרא </span><span dir=LTR>Minimum Infected to Start</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span>, שבמקרה הנוכחי ערכו נקבע ל- 10, אולם ניתן כמובן לשינוי. </span><span
        dir=LTR>Choose Comparison Column</span><span dir=RTL></span><span lang=HE
        style='font-family:"Arial",sans-serif'><span dir=RTL></span> מאפשר לבחור את
        המדד להשוואה בין המדינות מתוך מגוון רחב של משתני המגפה (מספר מקרים מאומתים,
        חולים קשים, מקרי מוות, מספר בדיקות, שיעורים של נתונים אלו למילון תושבים ורבים
        אחרים).</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>אם נגלול למטה נוכל
        לראות תמיד את השוואת מקדמי ההדבקה ולאחר מכן את השוואת מקדמי ההכפלה, שהינם
        טרנספורמציה של מקדמי ההדבקה (ראה דיון במאמר של </span><b><span dir=LTR
        style='font-family:"Times New Roman",serif'>Michael Beenstock</span></b><span
        dir=RTL></span><b><span lang=HE style='font-family:"Times New Roman",serif'><span
        dir=RTL></span> &amp; </span></b><b><span dir=LTR style='font-family:"Times New Roman",serif'>Xieer
        Dai</span></b><span dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span>). </p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>במק</span><span
        lang=HE style='font-family:"Arial",sans-serif'>רה הנוכחי בחרנו לצורך השוואת
        מקדמי ההדבקה אוסף של מדינות שונות מהעולם עם כמויות מקרים שונות. בולט ביותר הוא
        הדימיון הרב בין תהליכי ההתפתחות של מקדם ההדבקה -  התפרצות מהירה עד יום כ-10 לכ –
        15, </span><span dir=LTR></span><span lang=HE dir=LTR><span dir=LTR></span> </span><span
        lang=HE style='font-family:"Arial",sans-serif'>ולאחר מכן תהליך דעיכה איטי יותר
        המתקרב  לערך הקרוב לחצי עד קרוב ל-0 בין הימים 55 ל-65.</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span dir=LTR><img width=700 height=300 id="Picture 3"
        src="https://github.com/gstat-gcloud/covid19-sim/raw/master/gstat_app/src/assets/images/image003.jpg"
        alt="A screenshot of a cell phone&#10;&#10;Description automatically generated"></span></p>
        
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'> </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>  </span><span
        lang=HE style='font-family:"Arial",sans-serif'> </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>הגרף הבא לקוח מתוך
        המאמר של () ומציג  את השוואת מקדמי ההדבקה בפרובינציות של סין בין תחילת
        ינואר לאמצע אפריל 2020.</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span dir=LTR><img width=700 height=300 id="Picture 4"
        src="https://github.com/gstat-gcloud/covid19-sim/raw/master/gstat_app/src/assets/images/image005.jpg"
        alt="A screenshot of a cell phone&#10;&#10;Description automatically generated"></span></p>
        
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>גם כאן אנו רואים
        תמונה דומה ביותר של התפתחות המגפה, כאשר מבחינים בגל שני בהונג קונג. </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'> </span></p>
        
        <h2 dir=RTL style='margin-top:2.0pt;margin-right:.4in;margin-bottom:0in;
        margin-left:0in;margin-bottom:.0001pt;text-align:right;direction:rtl;
        unicode-bidi:embed'><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'>תהליך חיזוי
        </span><span dir=LTR style='font-family:"Arial",sans-serif'>R</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> ומדדי המגפה לישראל  </span></h2>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>הבסיס לחיזוי של
        מדדי מחלת הקורונה לישראל מבוסס על לימוד ערכי </span><span dir=LTR>R</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> במדינות שבהן המגפה בשלבים מתקדמים יותר במידה זו או אחרת מאשר בישראל.
        תהליך החיזוי מתבצע על ידי בחירת המדינות שיהיו הבסיס לחיזוי ערכי </span><span
        dir=LTR>R</span><span dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> העתידיים בישראל. </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>על מנת לבחור ולאתר
        מדינות דומות לישראל מבחינת מדיניות השחרור ניתן לבחור מדינות שבהן מדד אוקספורד
        למצב הנוכחי של חומרת הצעדים נמצא בטווח נתון בטווח ימים נתון בעבר. בחירה בטווח
        מסויים של מדד אוקספורד נעשית באמצעות הסליידר והמערכת מציגה באופן אוטומטי בגרף
        את ערכי </span><span dir=LTR>R</span><span dir=RTL></span><span lang=HE
        style='font-family:"Arial",sans-serif'><span dir=RTL></span> למדינות העונות לערכים
        אלו. במקביל
        נעשה חישוב נוסף. לכל יום קורונה עתידי מחושב הממוצע של מקדם ההדבקה במדינות
        שנבחרו ומונח שזה יהיה ערכו בעתיד בכל יום קורונה עתידי בישראל. בדרך זו אנו חוזים
        את </span><span dir=LTR>R</span><span dir=RTL></span><span lang=HE
        style='font-family:"Arial",sans-serif'><span dir=RTL></span> ומתחזית זו נגזרות
        גם התחזיות של כל שאר המדדים. בררת המחדל לתחזית המוצגת היא  תחזית מספר החולים
        הקשים בכל יום עתידי בישראל, המהווה חסם עליון לכמות המונשמים, שהינו משתנה הבקרה
        העיקרי למדיניות. </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span dir=LTR><img width=700 height=300 id="Picture 3"
        src="https://github.com/gstat-gcloud/covid19-sim/raw/master/gstat_app/src/assets/images/image007.jpg"
        alt="A screenshot of a cell phone&#10;&#10;Description automatically generated"></span></p>
    
        <p class=MsoNormal dir=RTL style='margin-top:-0.65in;text-align:right;direction:rtl;unicode-bidi:
        embed'><span dir=LTR><img width=700 height=300 id="Picture 3"
        src="https://github.com/gstat-gcloud/covid19-sim/raw/master/gstat_app/src/assets/images/image009.jpg"
        alt="A screenshot of a cell phone&#10;&#10;Description automatically generated"></span></p>
        
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'> </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>  </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>ניתן לבחור קבוצת
        מדינות הכוללת מדינות שהיה בהן גל שני של התפרצות בשילוב עם מדינות ללא גל שני,
        ולקבל תחזית של תרחיש ממוצע. ניתן לבחור רק את המדינות שבהן היה גל שני ולקבל
        אינדיקטורים למה יקרה בישראל במצב של גל שני, בהנחה שהמהלך יהיה דומה למדינות
        ההתיחסות שבהן היה גל שני. המשתמש יכול לבחור להשוואה מדינות ספציפיות עם מדיניות
        שחרור ספציפית (חזרה לבית ספר מלאה, רק גני ילדים וכד.), על בסיס מידע חיצוני,
        ולהתבסס עליהן בחיזוי משתני הקורונה בישראל.</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>נציג להדגמה שלושה
        תרחישים שערכנו לחיזוי משתני הקורונה בישראל, במהלך חודש מאי 2020, באמצעות המערכת
        - אופטימי, ממוצע ופסימי.</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
    
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif;color:#5B9BD5'>תרחיש
        אופטימי: תחזיות מדדי קורונה בישראל על בסיס מהלך המגפה בסין</span><span dir=LTR></span><span
        dir=LTR style='font-family:"Arial",sans-serif;color:#5B9BD5'><span dir=LTR></span>,</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif;color:#5B9BD5'><span
        dir=RTL></span> דרום קוריאה ושווצריה.</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span dir=LTR><img width=700 height=300 id="Picture 3"
        src="https://github.com/gstat-gcloud/covid19-sim/raw/master/gstat_app/src/assets/images/image011.jpg"
        alt="A screenshot of a cell phone&#10;&#10;Description automatically generated"></span></p>
        
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif;color:#5B9BD5'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif;color:#5B9BD5'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>בהנחה שהמשך
        ההתפתחות בישראל יהיה כמו בשלושת המדינות הללו, שבהן לא הייתה התפרצות של גל שני, אנו
        חוזים כמות של 30 חולים קשים בלבד בסוף מאי 2020.</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif;color:#5B9BD5'>תרחיש
        ממוצע: התפתחות המגפה בישראל תהיה דומה לממוצע במדינות ללא גל שני (סין, דרום
        קוראה ושווצריה) ומדינות שבהן היה גל שני (הונג קונג וסינגפור).</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span dir=LTR><img width=700 height=300 id="Picture 3"
        src="https://github.com/gstat-gcloud/covid19-sim/raw/master/gstat_app/src/assets/images/image014.jpg"
        alt="A screenshot of a cell phone&#10;&#10;Description automatically generated"></span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span dir=LTR>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span dir=LTR>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>בתרחיש זה ישנה
        עלייה בכמות החולים הקשים החזויה לסוף מאי 2020 לישראל, אולם לרמה של קצת מעל ל-
        50, מספר שהינו עדיין נמוך ביותר.</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
            
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif;color:#5B9BD5'>תרחיש
        פסימי: תחזית מבוססת רק על מדינות שחוו גל שני – הונג קונג וסינגפור</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span dir=LTR><img width=700 height=300 id="Picture 3"
        src="https://github.com/gstat-gcloud/covid19-sim/raw/master/gstat_app/src/assets/images/image016.jpg"
        alt="A screenshot of a cell phone&#10;&#10;Description automatically generated"></span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>בתרחיש זה כמות
        החולים הקשים בסוף מאי תתקרב ל- 100, בערך כמו בסוף אפריל 2020. גם מספר זה נמוך
        ובר הכלה. יש לשים לב שגם בהונג קונג ובסינגפור הגל השני לא התפרץ לרמות גבוהות  הדומות
        לשיאי מקדמי ההידבקות בהתפרצויות הגל הראשון בישראל, סין ובמדינות אירופה וארה&quot;ב.
        כמו כן בהונג קונג הגל השני נבלם מזמן ובסינגפור הגל השני גם במגמת ירידה. בשתי המדינות
        הגל השני נבע מטעויות ביישום המדיניות. בהונג קונג, לאחר סיום הגל הראשון, לא
        נעשתה בקרה הדוקה על טיסות שנחתו מאירופה, וההתפרצות מיוחסת ברובה ליבוא מאירופה
        של חולי קורונה. הערכות מהירה בלמה את הגל. סינגפור התחילה במדיניות סגרים וניטור
        דומה לזו של דרום קוריאה אולם היישום היה לקוי. ההתפרצות הנוכחית בסינגפור נבעה מהתפשטות
        מהירה של הנגיף בקרב פועלים זרים שמתגוררים ביחד בצפיפות רבה. מקרים ראשונים
        שאירעו במעונות אלו הוזנחו, ובדומה לבתי אבות בכל העולם, נרשמה במעונות אלו התפרצות
        מהירה ביותר. </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>אם מדינת ישראל
        תנהיג מדיניות כניסה קפדנית לישראל ותאתר מהר מוקדי התפרצות חדשים הסיכוי לגל שני
        בישראל בדומה לסינגפור והונג קונג הינו קטן ביותר. </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:right;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <h1 dir=RTL style='margin-top:2.0pt;margin-right:.4in;margin-bottom:0in;
        margin-left:0in;margin-bottom:.0001pt;text-align:right;direction:rtl;
        unicode-bidi:embed'><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'>סיכום</span></h2>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>הדגמנו את דרך
        השימוש במערכת </span><span dir=LTR>GstatCOVID</span><span dir=RTL></span><span
        lang=HE style='font-family:"Arial",sans-serif'><span dir=RTL></span> להערכת
        הסיכוי להתפרצות של גל שני של מגפת הקורונה בישראל ולהיקף הצפוי של החולים הקשים
        בהתפרצות, בעקבות תהליכי שחרור המשק. הניתוח התבסס על הניסיון הידוע כיום בעולם
        ממדינות שהחלו תהליכי שחרור לפני ישראל. מהניתוח עולה שגם אם המצב בישראל יהיה
        דומה למדינות שבהם נרשם גל שני, התוצאות יהיו ברמה ברת הכלה והקפדה על צעדי
        מדיניות קפדניים בנמל תעופה בן גוריון וניהול סגרים מהיר במוקדי התפרצות חדשים
        יקטינו לרמה נמוכה ביותר את הסיכוי להתפרצות מחודשת.</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>במהלך פתוח המערכת
        בחנו מודלים שונים וגישות שונות. בחרנו לבסוף בגישת הניבוי שנראתה לנו כטובה ביותר
        מבחינת היכולת לחזות את העתיד ומבחינת מיצוי נכון של המידע החלקי הקיים כיום בעולם
        על תהליכי השחרור מאמצעי המדיניות. </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>אנו מצפים ומקווים
        לקבל ביקורת על המודל ודרך יישומו. אנו משוכנעים שיש דרכים לא פחות טובות משלנו לבצע
        את החיזוי. </span><span dir=LTR>GstatCOVID</span><span dir=RTL></span><span
        lang=HE style='font-family:"Arial",sans-serif'><span dir=RTL></span> הינה
        פלטפורמה המאפשרת יישום במקביל של מספר מודלים. אנו מזמינים את כל מי שפתח מודלים
        בתחום ורוצה לחשוף אותם לציבור, להעלות אותם למערכת </span><span dir=LTR>GstatCOVID</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span>. אנו יודעים כיום מתחרויות </span><span dir=LTR>KAGGLE</span><span
        dir=RTL></span><span lang=HE style='font-family:"Arial",sans-serif'><span
        dir=RTL></span> שהמודלים בעלי כושר הניבוי הטוב ביותר היו ברוב המקרים אלו 
        ששילבו מספר גישות חיזוי שונות.</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>שילוב מודלים לקבלת
        הניבוי הטוב ביותר, דיון ציבורי על המודלים, ודיונים מקצועיים על ההנחות והמתודות
        יכולים לשפר את טיב הניבויים, וזאת בניגוד למצב שבו נעשה שימוש במודלים שלא נחשפים
        לביקורת ציבורית ומקצועית. </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span dir=LTR>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span dir=LTR>&nbsp;</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>אנו מודים לאלישע סטוין
        ושאר עובדי המודיעין על התמיכה והליווי שקיבלנו מהם במהלך הפתוח. </span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>להסברים ולהבהרות
        בנושא המערכת והמודלים  ניתן להפנות למפתח המערכת דן פלדמן (והרבה תודות לו ולשאר
        צוות המתנדבים מ- </span><span dir=LTR>Gstat</span><span dir=RTL></span><span
        lang=HE style='font-family:"Arial",sans-serif'><span dir=RTL></span> שעבדו עימו:
        אלישר חודרוב, רועי עסיס, עוז מזרחי ועינב פיטרמן ואניה סורקין)</span></p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span lang=HE style='font-family:"Arial",sans-serif'>&nbsp;</span></p>
        
        <p class=MsoNormal style='text-align:justify'>&nbsp;</p>
        
        <p class=MsoNormal dir=RTL style='text-align:justify;direction:rtl;unicode-bidi:
        embed'><span dir=LTR>&nbsp;</span></p>
        
    
        """, unsafe_allow_html=True
    )