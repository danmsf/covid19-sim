# Updating App Instructions

### Adding a New Model:
This app is designed with modularity in mind.  
You are the owner of your own model (for the most part)...  
To add a new model:

1. Create `model_yours.py` file and save it in `src/shared/models` containing:
   *  `YourModel` class
        - containing your models functionality
   * `YourModelParameters` class
        - simple class to define your models input paramters
2. Add your default settings to `src/shared/defaults.yaml` file
3. Create `presentModel.py` file and save it in `src/pages/models` containing:
   * call `DEFAULTS` from `/src/shared/settings` to access your default settings
   * a `write()` function
        - with all the logic you want to display in your model
        - this is the `main` part of your code
        - you'll need to call `display_sidebar` here...
   * a `display_sidebar()` function
        - giving access to the parameters you want changed
4. Update `MODELS` in `src\pages\projections.py` so your model can be chosen

And that's it!

## Adding charts
You'll probably want custom charts for your model. 
 
Just save them in `src/shared/charts/charts_yourmodel.py`  
so you can call them from `presentModel.py` (your presentation)

 ## Updating a models parameters
 * Just change in `src/shared/defaults.yaml` file

## Adding a table data source
In general, data should be called through a `class` in the `src/shared/models/data.py` file.  

You should load your data through a `cached` function in `src/shared/settings.py`
If you create your data there, you can import it to your presentation file by name.