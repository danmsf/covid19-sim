"""Utils."""
import streamlit as st
from collections import namedtuple
from datetime import datetime, timedelta
from typing import Optional
from base64 import b64encode
import io
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import streamlit.ReportThread as ReportThread
from streamlit.server.Server import Server
import time
import functools
# import random
# import string
# from .parameters import Parameters


# (0.02, 7) is 2%, 7 days
# be sure to multiply by 100 when using as a default to the pct widgets!
RateLos = namedtuple("RateLos", ("rate", "length_of_stay"))


def add_date_column(
        df: pd.DataFrame, drop_day_column: bool = False, date_format: Optional[str] = None,
) -> pd.DataFrame:
    """Copies input data frame and converts "day" column to "date" column

    Assumes that day=0 is today and allocates dates for each integer day.
    Day range can must not be continous.
    Columns will be organized as original frame with difference that date
    columns come first.

    Arguments:
        df: The data frame to convert.
        drop_day_column: If true, the returned data frame will not have a day column.
        date_format: If given, converts date_time objetcts to string format specified.

    Raises:
        KeyError: if "day" column not in df
        ValueError: if "day" column is not of type int
    """
    if not "day" in df:
        raise KeyError("Input data frame for converting dates has no 'day column'.")
    if not pd.api.types.is_integer_dtype(df.day):
        raise KeyError("Column 'day' for dates converting data frame is not integer.")

    df = df.copy()
    # Prepare columns for sorting
    non_date_columns = [col for col in df.columns if not col == "day"]

    # Allocate (day) continous range for dates
    n_days = int(df.day.max())
    start = datetime.now()
    end = start + timedelta(days=n_days + 1)
    # And pick dates present in frame
    dates = pd.date_range(start=start, end=end, freq="D")[df.day.tolist()]

    if date_format is not None:
        dates = dates.strftime(date_format)

    df["date"] = dates

    if drop_day_column:
        df.pop("day")
        date_columns = ["date"]
    else:
        date_columns = ["day", "date"]

    # sort columns
    df = df[date_columns + non_date_columns]

    return df


def dataframe_to_base64(df: pd.DataFrame) -> str:
    """Converts a dataframe to a base64-encoded CSV representation of that data.

    This is useful for building datauris for use to download the data in the browser.

    Arguments:
        df: The dataframe to convert
    """
    csv = df.to_csv(index=False)
    b64 = b64encode(csv.encode()).decode()
    return b64


def pivot_dataframe(df, col_name, countryname, normalize_day=False):
    """Convert DataFrame to Pivot view"""
    piv_temp = pd.DataFrame(index=pd.date_range(start=df.index.min(), end=df.index.max())).reset_index(drop=True)
    for country in countryname:
        if normalize_day:
            piv_temp = (piv_temp.join(df[(df.Country == country)&
                                     (df['total_cases']>=normalize_day)].reset_index(drop=True)
                                      .pivot(columns='Country', values=col_name)))
        else:
            piv_temp = (piv_temp.join(df[(df.Country == country)].reset_index(drop=True)
                                      .pivot(columns='Country', values=col_name)))

    return piv_temp

def get_table_download_link(df, name):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{name}.csv">Download {name}</a>'
    return href

def get_repo_download_link(filename, desc):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    href = f'<a href="https://github.com/gstat-gcloud/covid19-sim/raw/master/Resources/{filename}" download  >Download {desc}</a>'
    return href

def display_about(st):

    st.sidebar.markdown("This app was developed in pure python utilizing the awesome [streamlit](https:\\streamlit.io) library.  "
                        "For other inspiring ideas see [Penn University Covid](https://penn-chime.phl.io) "
                        "or for more general applications [Awesome Streamlit](https://awesome-streamlit.org/)")

    st.sidebar.info(
        """
        This tool is maintained by `dan.feldman@g-stat.com`  
        Feel free to contact me for explanations or if you encounter any problems.
        """
    )
    st.sidebar.info("Thanks to everyone who volounteered to help develop and mantain this app, including (but not limited to):  "
            "Elisar Chodorov, "
            "Oz Mizrahi, "
            "Roy Assis, "
            "Dan Feldman, "
            "Ephraim Goldin, "
            "Annia Sorokin, "
            "Laura Lerner, and anyone else I missed :) ")


# Copied from tvst's great gist:
# https://gist.github.com/tvst/6ef6287b2f3363265d51531c62a84f51
def get_session_id():
    # Hack to get the session object from Streamlit.

    ctx = ReportThread.get_report_ctx()

    session = None
    # session_infos = Server.get_current()._session_infos.values()
    session_infos = Server.get_current()._session_info_by_id.values()
    for session_info in session_infos:
        s = session_info.session
        if (
            (hasattr(s, '_main_dg') and s._main_dg == ctx.main_dg)
            # Streamlit < 0.54.0
            or
            # Streamlit >= 0.54.0
            (not hasattr(s, '_main_dg') and s.enqueue == ctx.enqueue)
        ):
            session = session_info.session

    if session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')

    return id(session)

def fancy_cache(func=None, ttl=None, unique_to_session=False, **cache_kwargs):
    """A fancier cache decorator which allows items to expire after a certain time
    as well as promises the cache values are unique to each session.
    Parameters
    ----------
    func : Callable
        If not None, the function to be cached.
    ttl : Optional[int]
        If not None, specifies the maximum number of seconds that this item will
        remain in the cache.
    unique_to_session : boolean
        If so, then hash values are unique to that session. Otherwise, use the default
        behavior which is to make the cache global across sessions.
    **cache_kwargs
        You can pass any other arguments which you might to @st.cache
    """
    # Support passing the params via function decorator, e.g.
    # @fancy_cache(ttl=10)
    if func is None:
        return lambda f: fancy_cache(
            func=f,
            ttl=ttl,
            unique_to_session=unique_to_session,
            **cache_kwargs
        )

    # This will behave like func by adds two dummy variables.
    dummy_func = st.cache(
        func = lambda ttl_token, session_token, *func_args, **func_kwargs: \
            func(*func_args, **func_kwargs),
        **cache_kwargs)

    # This will behave like func but with fancy caching.
    @functools.wraps(func)
    def fancy_cached_func(*func_args, **func_kwargs):
        # Create a token which changes every ttl seconds.
        ttl_token = None
        if ttl is not None:
            ttl_token = int(time.time() / ttl)

        # Create a token which is unique to each session.
        session_token = None
        if unique_to_session:
            session_token = get_session_id()

        # Call the dummy func
        return dummy_func(ttl_token, session_token, *func_args, **func_kwargs)
    return fancy_cached_func

# def fancy_cache_demo():
#     """Shows how to use the @fancy_cache decorator."""
#
#     st.write('## ttl example')
#
#     @fancy_cache(ttl=1)
#     def get_current_time():
#         return time.time()
#     for i in range(10):
#         st.write("This number should change once a second: `%s` (iter: `%i`)" %
#             (get_current_time(), i))
#         time.sleep(0.2)
#
#     st.write('## unique_to_session example')
#
#     @fancy_cache(unique_to_session=True)
#     def random_string(string_len):
#         return ''.join(random.sample(string.ascii_lowercase, string_len))
#     for i in range(3):
#         st.write("This string shouldn't change, but should differ by session: `%s` (iter: `%i`)" %
#             (random_string(10), i))
#

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

