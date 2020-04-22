# Updating App Instructions

### Adding a New Model:
There are 5 places you need to make changes when you add a new model:  
(You'll have an easier time if you fold all the code on the page before you begin ....)
 1. Save the code to model in `models.py` 
    * Make your model a `class` that accepts `p` of class `Parameters`
    * acces your model parameters as a dictionary stored in `p`  
    For example:        
        ````
       class NewModel:
            def __init__(self, p: Parameters):
                self.beta = p.NewModel_params['beta']
                self.time = p.NewModel_params['times']
       ````
    * If your model returns a DataFrame save it in a atrribute (i.e. `self.df = output`)  
 
 2. Add your model parameters in the file `defaults.py`:
    * Declare it in the `Constants` class
    in the `def __init()` as a required input
    * And assign it as an attribute 
    * **Don't put your default values here**  
    For example:
    ```
    class Constant:
        def __init__(
                        self,
                        *,
                        NewModel_params
                    ): 
     
            self.NewModel_params = NewModel_params
    ``` 
 3. Add your default value to te file `settings.py`:
    * This is where you assign your default values in a dict form  
    For example:
    ```
    DEFAULTS = Constants(
                         NewModel_params = {`beta`:0.5,
                                            `times`: 150}
                         )   
    ```
  4. To make yor model interactive you need to add your models parameters as a **dictionary** in the `Parameters` class in the  `parameters.py` file  
     For example:
     ```
     class Parameters:
        def __init__(
                        self,
                        *,
                        NewModel_params
                    ): 
     
            self.NewModel_params = NewModel_params
     
     ```
  5. Add your model parameters to the `display_sidebar` function in `presentation.py`
        * save the output of your selection to the same dict
        * save the output of that dict to the `return Parameters`
        * Make your parameters show on condition of your model being chosen  
        For example:
        ```
        def display_sidebar(st, d: Constants, models_option=None):
            ...
            ...
            ...
            if "My New Model Name" in models_option:
                d.NewModel_params['beta'] = st.sidebar.number_input(
                                                            "Chose beta",
                                                            min_value=0.01,
                                                            value=d.NewModel_params['beta'],
                                                            step=0.025,
                                                            format="%f",
                                                            )
                d.NewModel_params['times'] = st.sidebar.number_input(
                                            "Chose beta",
                                            min_value=10,
                                            value=d.NewModel_params['times'],
                                            step=1,
                                            format="%i",
                                            )

        return Parameters(
                            ...
                            ...
                            NewModel_params = d.NewModel_params
                            )
        ```
 6. Finaly, you can call your model and use it in the `app.py` file
    * Add your model name to :
    ``` 
    models_option = st.sidebar.multiselect(
    'Which models to show?',
    ('Penn Dashboard', 'OLG Model', 'SEIAR Model', 'SEIRSPlus', 'New Model Name'), )
    ```
    * Call your model under a condition:
    ``` 
    if "New Model Name" in model_options:
        new_model = NewModel(p)
        ...
        <Plot or show table>
    ```
 ## Updating a models paramters
 * If you want to change the default values do so in step `3.` above.
 * If you want to add more parameters update the dict in  `3.` and `5.`
 * If you want to add a parameter not in the dict, `2`, `3` and `5`
 
## Updating a graph         
If the graph is complicated its best to do so in `charts.py`.

## Adding a table data source
In general, data should be called through a `class` in the `models.py`
 file.  
The filename can be accessed directly from `DEFAULTS` so you only need to do steps `2.` and `3.` above.
  