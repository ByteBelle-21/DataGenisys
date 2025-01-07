# DataGenisys

Data Predictify is a data science project where I apply my computer science skills to build predictive models using Kaggle’s Alzheimer’s Disease Dataset. The project focuses on analyzing the data, applying machine learning techniques, and predicting the progression of Alzheimer’s disease. Key aspects include data preprocessing, feature engineering, model selection, and performance evaluation, with the aim of generating valuable insights into the disease's progression.I have developed this website to show the resuls of data processing,visualization and predictive model.

For the data science project, the backend is built using Django with Python, providing a robust framework for web development. Data manipulation and analysis are handled with Pandas, enabling efficient data processing and transformation. Scikit-learn is utilized for building machine learning models, while Seaborn and Matplotlib are used for data visualization, allowing for clear and insightful graphical representations of the results. This combination of technologies ensures a seamless workflow for data analysis and model development.

------------------------------------------------------------
Citation for the dataset  -  Alzheimer’s Disease Dataset

@misc{rabie_el_kharoua_2024,
title={Alzheimer's Disease Dataset},
url={https://www.kaggle.com/dsv/8668279},
DOI={10.34740/KAGGLE/DSV/8668279},
publisher={Kaggle},
author={Rabie El Kharoua},
year={2024}
}

-----------------------------------------------------------


To run the application, plaese ensure that you have python3 in your system . 
After cloning the git repository, navigate through directories using ` cd dataGenisys/dataScience/ ` .
To ensure that you are in correct directory, plaese make sure file `manage.py` is in the current directory. 
Run command ` python3 -m pip install -r requirement.txt ` to install the dependencies 
Run `python3 manage.py migrate` and then ` python3 manage.py runserver ` to start the application. 
The applicartion will be available on port 8000. 

To test the applcation, you can provide the required data in the following form as a comma separated values
Required field - 
Age, Gender, Ethnicity, EducationLevel, BMI, Smoking, AlcoholConsumption, PhysicalActivity, DietQuality, SleepQuality, FamilyHistoryAlzheimers, CardiovascularDisease, Diabetes, Depression, HeadInjury, Hypertension, SystolicBP, DiastolicBP, CholesterolTotal, CholesterolLDL, CholesterolHDL, CholesterolTriglycerides, MMSE, FunctionalAssessment, MemoryComplaints, BehavioralProblems, ADL, Confusion, Disorientation, PersonalityChanges, DifficultyCompletingTasks, Forgetfulness
Example input -
73,Male,Caucasian,Bachelor's,22.92774923,No,13.29721773,6.327112474,1.347214306,9.025678666,No,No,Yes,Yes,No,No,142,72,242.3668397,56.15089696,33.6825635,162.1891431,21.46353236,6.518876973,No,No,1.72588346,No,No,No,Yes,No

The result will be whether the patient have Alzheimer’s disease or not. 



