"""
ETL Pipeline for IT Job Data Analysis
This script extracts, transforms, and loads IT-relevant job data from multiple CSV files
to create a consolidated dataset for future analysis and prediction.
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ITJobETL:
    def __init__(self, base_path="a:/SUMMER_2025/archive_Term_project"):
        self.base_path = base_path
        self.it_keywords = [
            # Programming Languages
            'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'scala',
            'kotlin', 'swift', 'typescript', 'sql', 'r', 'matlab', 'perl', 'bash', 'powershell',
            
            # Technologies & Frameworks
            'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'laravel',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'cloud', 'devops', 'ci/cd', 'jenkins',
            'git', 'github', 'gitlab', 'linux', 'unix', 'windows server', 'vmware', 'terraform',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle', 'sql server',
            'elasticsearch', 'nosql', 'database', 'dba', 'data warehouse', 'etl',
            
            # AI/ML/Data Science
            'machine learning', 'artificial intelligence', 'deep learning', 'neural network',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'jupyter', 'data science',
            'data analysis', 'data mining', 'big data', 'hadoop', 'spark', 'kafka', 'tableau',
            'power bi', 'analytics', 'statistics', 'nlp', 'computer vision',
            
            # Web Development
            'html', 'css', 'bootstrap', 'jquery', 'rest api', 'graphql', 'microservices',
            'web development', 'full stack', 'frontend', 'backend', 'ui/ux', 'responsive design',
            
            # Mobile Development
            'android', 'ios', 'mobile development', 'react native', 'flutter', 'xamarin',
            
            # Security
            'cybersecurity', 'information security', 'network security', 'penetration testing',
            'ethical hacking', 'security analysis', 'firewall', 'encryption', 'ssl', 'vpn',
            
            # Networking
            'network', 'cisco', 'routing', 'switching', 'tcp/ip', 'dns', 'dhcp', 'load balancer',
            
            # Project Management
            'agile', 'scrum', 'kanban', 'jira', 'confluence', 'project management',
            
            # General IT
            'software', 'hardware', 'system', 'technical', 'programming', 'coding', 'development',
            'engineer', 'developer', 'analyst', 'architect', 'administrator', 'consultant',
            'it support', 'help desk', 'troubleshooting', 'maintenance', 'infrastructure'
        ]
        
        self.it_job_titles = [
            'software engineer', 'data scientist', 'web developer', 'mobile developer',
            'devops engineer', 'system administrator', 'database administrator', 'network engineer',
            'security analyst', 'cybersecurity', 'machine learning', 'ai engineer', 'cloud engineer',
            'full stack', 'frontend', 'backend', 'qa engineer', 'test engineer', 'product manager',
            'technical lead', 'engineering manager', 'solution architect', 'data engineer',
            'data analyst', 'business intelligence', 'it consultant', 'technical support',
            'system analyst', 'software architect', 'platform engineer', 'site reliability',
            'automation engineer', 'infrastructure engineer', 'application developer',
            'programmer', 'developer', 'analyst', 'engineer', 'architect', 'administrator'
        ]
        
    def is_it_related(self, text):
        """Check if text is IT-related based on keywords and job titles"""
        if pd.isna(text):
            return False
            
        text_lower = str(text).lower()
        
        # Check for IT keywords
        for keyword in self.it_keywords:
            if keyword in text_lower:
                return True
                
        # Check for IT job titles
        for title in self.it_job_titles:
            if title in text_lower:
                return True
                
        return False
    
    def load_data(self):
        """Load all relevant CSV files"""
        print("Loading data files...")
        
        # Load smaller files first
        try:
            self.companies = pd.read_csv(f"{self.base_path}/companies/companies.csv")
            self.company_industries = pd.read_csv(f"{self.base_path}/companies/company_industries.csv")
            self.job_skills = pd.read_csv(f"{self.base_path}/jobs/job_skills.csv")
            self.job_industries = pd.read_csv(f"{self.base_path}/jobs/job_industries.csv")
            self.benefits = pd.read_csv(f"{self.base_path}/jobs/benefits.csv")
            self.salaries = pd.read_csv(f"{self.base_path}/jobs/salaries.csv")
            
            print(f"Loaded companies: {len(self.companies)} records")
            print(f"Loaded company_industries: {len(self.company_industries)} records")
            print(f"Loaded job_skills: {len(self.job_skills)} records")
            print(f"Loaded job_industries: {len(self.job_industries)} records")
            print(f"Loaded benefits: {len(self.benefits)} records")
            print(f"Loaded salaries: {len(self.salaries)} records")
            
        except Exception as e:
            print(f"Error loading smaller files: {e}")
            return False
            
        return True
    
    def load_postings_chunk(self, chunk_size=10000):
        """Load large postings file in chunks and filter for IT jobs"""
        print("Loading and filtering job postings...")
        
        it_postings = []
        chunk_count = 0
        total_processed = 0
        it_jobs_found = 0
        
        try:
            # Read in chunks
            for chunk in pd.read_csv(f"{self.base_path}/postings.csv", chunksize=chunk_size):
                chunk_count += 1
                total_processed += len(chunk)
                
                # Filter for IT-related jobs
                it_mask = (
                    chunk['title'].apply(self.is_it_related) |
                    chunk['description'].apply(self.is_it_related) |
                    chunk['skills_desc'].apply(self.is_it_related)
                )
                
                it_chunk = chunk[it_mask]
                it_jobs_found += len(it_chunk)
                
                if len(it_chunk) > 0:
                    it_postings.append(it_chunk)
                
                if chunk_count % 10 == 0:
                    print(f"Processed {chunk_count} chunks ({total_processed:,} records), "
                          f"Found {it_jobs_found:,} IT jobs so far...")
                    
        except Exception as e:
            print(f"Error loading postings: {e}")
            return None
            
        if it_postings:
            self.postings = pd.concat(it_postings, ignore_index=True)
            print(f"Final IT job postings: {len(self.postings):,} records")
            return True
        else:
            print("No IT job postings found!")
            return False
    
    def filter_it_companies(self):
        """Filter companies to include only those with IT focus or IT job postings"""
        print("Filtering IT-related companies...")
        
        # Companies with Technology industry focus
        tech_companies = self.companies[self.companies['industry_focus'] == 'Technology']['company_id'].tolist()
        
        # Companies that have IT job postings
        companies_with_it_jobs = self.postings['company_id'].unique().tolist()
        
        # Combine both lists
        all_it_companies = list(set(tech_companies + companies_with_it_jobs))
        
        # Filter companies
        self.it_companies = self.companies[self.companies['company_id'].isin(all_it_companies)]
        
        print(f"IT companies identified: {len(self.it_companies)}")
    
    def create_skills_mapping(self):
        """Create a mapping of skill abbreviations to full names"""
        # Common IT skill mappings
        skill_mapping = {
            'PYTHON': 'Python Programming',
            'JAVA': 'Java Programming',
            'JS': 'JavaScript',
            'SQL': 'SQL Database',
            'AWS': 'Amazon Web Services',
            'DOCKER': 'Docker Containerization',
            'K8S': 'Kubernetes',
            'REACT': 'React.js',
            'ANGULAR': 'Angular Framework',
            'NODE': 'Node.js',
            'SPRING': 'Spring Framework',
            'DJANGO': 'Django Framework',
            'FLASK': 'Flask Framework',
            'AI': 'Artificial Intelligence',
            'ML': 'Machine Learning',
            'DATA': 'Data Analysis',
            'CLOUD': 'Cloud Computing',
            'DEVOPS': 'DevOps',
            'MOBILE': 'Mobile Development',
            'WEB': 'Web Development',
            'DB': 'Database Management',
            'SEC': 'Security',
            'UX': 'User Experience',
            'UI': 'User Interface',
            'QA': 'Quality Assurance',
            'SW': 'Software Development',
            'CS': 'Computer Science'
        }
        
        return skill_mapping
    
    def transform_data(self):
        """Transform and clean the IT data"""
        print("Transforming data...")
        
        # Filter job skills for IT jobs only
        it_job_ids = self.postings['job_id'].tolist()
        self.it_job_skills = self.job_skills[self.job_skills['job_id'].isin(it_job_ids)]
        
        # Filter salaries for IT jobs
        self.it_salaries = self.salaries[self.salaries['job_id'].isin(it_job_ids)]
        
        # Filter benefits for IT jobs
        self.it_benefits = self.benefits[self.benefits['job_id'].isin(it_job_ids)]
        
        # Filter job industries for IT jobs
        self.it_job_industries = self.job_industries[self.job_industries['job_id'].isin(it_job_ids)]
        
        # Clean salary data
        if not self.it_salaries.empty:
            self.it_salaries = self.it_salaries.dropna(subset=['salary_hourly', 'salary_yearly'])
            self.it_salaries = self.it_salaries[self.it_salaries['salary_yearly'] > 0]
        
        print(f"IT job skills: {len(self.it_job_skills):,}")
        print(f"IT salaries: {len(self.it_salaries):,}")
        print(f"IT benefits: {len(self.it_benefits):,}")
        print(f"IT job industries: {len(self.it_job_industries):,}")
    
    def create_consolidated_dataset(self):
        """Create a single consolidated IT dataset"""
        print("Creating consolidated IT dataset...")
        
        # Start with IT job postings as base
        consolidated = self.postings.copy()
        
        # Add company information
        consolidated = consolidated.merge(
            self.it_companies[['company_id', 'company_name', 'company_size', 'industry_focus']], 
            on='company_id', 
            how='left',
            suffixes=('', '_company_info')
        )
        
        # Aggregate skills for each job
        if not self.it_job_skills.empty:
            skills_agg = self.it_job_skills.groupby('job_id')['skill_abr'].apply(
                lambda x: ','.join(x.astype(str))
            ).reset_index()
            skills_agg.columns = ['job_id', 'required_skills']
            
            consolidated = consolidated.merge(skills_agg, on='job_id', how='left')
        
        # Add salary information
        if not self.it_salaries.empty:
            salary_info = self.it_salaries.groupby('job_id').agg({
                'salary_yearly': 'mean',
                'salary_hourly': 'mean'
            }).reset_index()
            
            consolidated = consolidated.merge(salary_info, on='job_id', how='left')
        
        # Clean and standardize data
        consolidated['posting_date'] = pd.to_datetime(consolidated['listed_time'], errors='coerce')
        consolidated['year'] = consolidated['posting_date'].dt.year
        consolidated['month'] = consolidated['posting_date'].dt.month
        
        # Extract experience level and work type
        consolidated['experience_level'] = consolidated['formatted_experience_level'].fillna('Not Specified')
        consolidated['work_type'] = consolidated['formatted_work_type'].fillna('Not Specified')
        
        # Create IT domain categories based on job titles and descriptions
        consolidated['it_domain'] = consolidated.apply(self.categorize_it_domain, axis=1)
        
        self.consolidated_dataset = consolidated
        print(f"Consolidated dataset created with {len(consolidated):,} IT job records")
    
    def categorize_it_domain(self, row):
        """Categorize jobs into IT domains"""
        title = str(row['title']).lower()
        desc = str(row['description']).lower()
        skills = str(row.get('required_skills', '')).lower()
        
        combined_text = f"{title} {desc} {skills}"
        
        # Define domain keywords
        domains = {
            'Software Development': ['software', 'developer', 'programming', 'coding', 'engineer', 'java', 'python', 'javascript', 'c++', 'c#'],
            'Data Science & Analytics': ['data scientist', 'data analyst', 'machine learning', 'ai', 'analytics', 'statistics', 'ml', 'deep learning'],
            'Web Development': ['web developer', 'frontend', 'backend', 'full stack', 'react', 'angular', 'vue', 'html', 'css'],
            'Mobile Development': ['mobile', 'android', 'ios', 'react native', 'flutter', 'swift', 'kotlin'],
            'DevOps & Cloud': ['devops', 'cloud', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'ci/cd', 'infrastructure'],
            'Cybersecurity': ['security', 'cybersecurity', 'penetration', 'firewall', 'encryption', 'security analyst'],
            'Database Administration': ['database', 'dba', 'sql', 'mysql', 'postgresql', 'oracle', 'mongodb'],
            'Network Engineering': ['network', 'cisco', 'routing', 'switching', 'tcp/ip', 'network engineer'],
            'Quality Assurance': ['qa', 'quality assurance', 'testing', 'test engineer', 'automation testing'],
            'IT Support & Administration': ['support', 'administrator', 'help desk', 'technical support', 'system admin'],
            'Product Management': ['product manager', 'technical lead', 'engineering manager', 'scrum master'],
            'UI/UX Design': ['ui', 'ux', 'user experience', 'user interface', 'design', 'figma']
        }
        
        # Check which domain matches
        for domain, keywords in domains.items():
            if any(keyword in combined_text for keyword in keywords):
                return domain
        
        return 'Other IT'
    
    def save_datasets(self):
        """Save the processed datasets"""
        print("Saving processed datasets...")
        
        # Save main consolidated dataset
        output_path = f"{self.base_path}/processed_it_jobs.csv"
        self.consolidated_dataset.to_csv(output_path, index=False)
        print(f"Saved consolidated IT dataset: {output_path}")
        
        # Save individual processed datasets
        self.it_companies.to_csv(f"{self.base_path}/processed_it_companies.csv", index=False)
        self.it_job_skills.to_csv(f"{self.base_path}/processed_it_skills.csv", index=False)
        
        if not self.it_salaries.empty:
            self.it_salaries.to_csv(f"{self.base_path}/processed_it_salaries.csv", index=False)
        
        if not self.it_benefits.empty:
            self.it_benefits.to_csv(f"{self.base_path}/processed_it_benefits.csv", index=False)
    
    def generate_summary_report(self):
        """Generate a summary report of the ETL process"""
        print("\n" + "="*60)
        print("IT JOB DATA ETL SUMMARY REPORT")
        print("="*60)
        
        print(f"\nOriginal Dataset Overview:")
        print(f"- Total Companies: {len(self.companies):,}")
        print(f"- IT-focused Companies: {len(self.it_companies):,}")
        print(f"- Total Job Skills Records: {len(self.job_skills):,}")
        print(f"- IT Job Skills Records: {len(self.it_job_skills):,}")
        
        print(f"\nIT Job Postings Analysis:")
        print(f"- Total IT Job Postings: {len(self.consolidated_dataset):,}")
        
        # Domain distribution
        domain_dist = self.consolidated_dataset['it_domain'].value_counts()
        print(f"\nIT Domain Distribution:")
        for domain, count in domain_dist.head(10).items():
            print(f"  - {domain}: {count:,} ({count/len(self.consolidated_dataset)*100:.1f}%)")
        
        # Experience level distribution
        exp_dist = self.consolidated_dataset['experience_level'].value_counts()
        print(f"\nExperience Level Distribution:")
        for level, count in exp_dist.head(5).items():
            print(f"  - {level}: {count:,} ({count/len(self.consolidated_dataset)*100:.1f}%)")
        
        # Work type distribution
        work_dist = self.consolidated_dataset['work_type'].value_counts()
        print(f"\nWork Type Distribution:")
        for work_type, count in work_dist.head(5).items():
            print(f"  - {work_type}: {count:,} ({count/len(self.consolidated_dataset)*100:.1f}%)")
        
        # Company size distribution
        size_dist = self.consolidated_dataset['company_size'].value_counts()
        print(f"\nCompany Size Distribution:")
        for size, count in size_dist.items():
            print(f"  - {size}: {count:,} ({count/len(self.consolidated_dataset)*100:.1f}%)")
        
        # Salary information
        if 'salary_yearly' in self.consolidated_dataset.columns:
            salary_data = self.consolidated_dataset['salary_yearly'].dropna()
            if len(salary_data) > 0:
                print(f"\nSalary Information (based on {len(salary_data):,} records):")
                print(f"  - Average Yearly Salary: ${salary_data.mean():,.0f}")
                print(f"  - Median Yearly Salary: ${salary_data.median():,.0f}")
                print(f"  - Salary Range: ${salary_data.min():,.0f} - ${salary_data.max():,.0f}")
        
        print("\n" + "="*60)
        print("ETL PROCESS COMPLETED SUCCESSFULLY!")
        print("="*60)

def main():
    """Main ETL execution function"""
    print("Starting IT Job Data ETL Pipeline...")
    print("="*50)
    
    # Initialize ETL processor
    etl = ITJobETL()
    
    # Execute ETL steps
    if not etl.load_data():
        print("Failed to load basic data files. Exiting.")
        return
    
    if not etl.load_postings_chunk():
        print("Failed to load job postings. Exiting.")
        return
    
    etl.filter_it_companies()
    etl.transform_data()
    etl.create_consolidated_dataset()
    etl.save_datasets()
    etl.generate_summary_report()
    
    print(f"\nProcessed files saved in: {etl.base_path}")
    print("Ready for analysis and prediction modeling!")

if __name__ == "__main__":
    main()
