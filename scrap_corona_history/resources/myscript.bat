call D:\Anaconda3\Scripts\activate.bat D:\Anaconda3 
D:
cd PycharmProjects\scrap_corona_history
call python "D:\PycharmProjects\scrap_corona_history\ETL_scrap_worldmeter.py"
call python "D:\PycharmProjects\scrap_corona_history\join_data_as_seir.py"