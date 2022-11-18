#!/usr/bin/env python
# coding: utf-8

# Install module

# In[74]:


get_ipython().system('{sys.executable} -m pip install pathlib2')


# In[75]:


import sys
get_ipython().system('{sys.executable} -m pip install smartnoise-sql')


# In[76]:


get_ipython().system('{sys.executable} -m pip install psycopg2-binary')


# In[122]:


privacy = Privacy(epsilon=0.01, delta=0.01)
meta_path = '/Users/kiringodhwani/Desktop/PUMS.yaml'

pumsdb = psycopg2.connect(user='postgres', host='localhost', database='ChicagoPolice')
reader = snsql.from_connection(pumsdb, privacy=privacy, metadata=meta_path)

#result = reader.execute('SELECT dac.category, COUNT(*) FROM public.data_allegation as da, public.data_allegationcategory as dac WHERE da.most_common_category_id = dac.id AND da.incident_date >= "2012-01-01" GROUP BY dac.category;')
#result = reader.execute('SELECT EXTRACT(year FROM incident_date) AS year, COUNT(*) AS number_of_incidents FROM public.lawsuit_lawsuit GROUP BY year')
result = reader.execute("SELECT COUNT(id) FROM data_officer WHERE race != 'Unknown' AND appointed_date >= '2010-01-01';")
#result = reader.execute("SELECT (SUM(CASE WHEN race = 'White' THEN 1 ELSE 0 END) / CAST(SUM(CASE WHEN race NOT IN ('White', 'Unknown') THEN 1 ELSE 0 END) AS float)) AS percent_poc FROM data_officer WHERE appointed_date > '2010-01-01';")
print(result)

result[1][0]


# In[119]:


print(np.arange(0.01,0.1,0.01))


# Python Script

# In[132]:


import snsql
from snsql import Privacy
import psycopg2
import matplotlib.pyplot as mpl
import numpy as np

epsilons = np.arange(0.01,0.1,0.01)
#epsilons = [0.00001,0.00005,0.0001,0.0005,0.001,0.005,0.01,0.05,0.1,0.2]
actual_value = 5419

x_axis_of_epsilons = []
errors = []
for i in epsilons:
    for j in range(10):
        privacy = Privacy(epsilon=0.01, delta=0.01)
        meta_path = '/Users/kiringodhwani/Desktop/PUMS.yaml'

        pumsdb = psycopg2.connect(user='postgres', host='localhost', database='ChicagoPolice')
        reader = snsql.from_connection(pumsdb, privacy=privacy, metadata=meta_path)
        result = reader.execute("SELECT COUNT(id) FROM data_officer WHERE race != 'Unknown' AND appointed_date >= '2010-01-01';")

        noised_ans = result[1][0]
        #percent_error = noised_ans
        percent_error = ((noised_ans - actual_value) / actual_value) * 100
        
        x_axis_of_epsilons.append(i)
        errors.append(percent_error)

mpl.scatter(x_axis_of_epsilons, errors)
        


# In[131]:


import time

#epsilons = np.arange(0.01,0.1,0.01)
epsilons = [0.00001,0.00005,0.0001,0.0005,0.001,0.005,0.01,0.05,0.1,0.2]
actual_value = 5419

x_axis_of_epsilons = []
runtimes = []
for i in epsilons:
    for j in range(10):
        privacy = Privacy(epsilon=0.01, delta=0.01)
        meta_path = '/Users/kiringodhwani/Desktop/PUMS.yaml'

        pumsdb = psycopg2.connect(user='postgres', host='localhost', database='ChicagoPolice')
        reader = snsql.from_connection(pumsdb, privacy=privacy, metadata=meta_path)
        
        start = time.time()
        result = reader.execute("SELECT COUNT(id) FROM data_officer WHERE race != 'Unknown' AND appointed_date >= '2010-01-01';")
        end = time.time()
        
        elapsed = end - start

        x_axis_of_epsilons.append(i)
        runtimes.append(elapsed)

mpl.scatter(x_axis_of_epsilons, errors)

