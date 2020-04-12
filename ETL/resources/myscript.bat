call D:\Anaconda3\Scripts\activate.bat D:\Anaconda3
D:
cd "D:\PycharmProjects\scrap_corona_history"
python "extract_worldmeter_data.py"
python "transform_worldmeter_data.py"
python "extract_gov_data.py"