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
        """, unsafe_allow_html=True)