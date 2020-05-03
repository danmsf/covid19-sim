import streamlit as st

def write():
    st.markdown(
        """
        

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