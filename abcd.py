from executors.naukri_executor import search_naukri_jobs
jobs = search_naukri_jobs("Data Scientist", max_jobs=10,headless=False)
for j in jobs:
    print(j)
