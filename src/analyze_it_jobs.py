"""
IT Job Market Analysis and Insights
This script analyzes the processed IT job data to identify trends, 
in-demand skills, and market opportunities.
Done by Vivian
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class ITJobAnalyzer:
    def __init__(self, data_path="a:/SUMMER_2025/archive_Term_project/processed_it_jobs.csv"):
        self.data_path = data_path
        self.df = None
        
    def load_data(self):
        """Load the processed IT job dataset"""
        print("Loading processed IT job dataset...")
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"Loaded {len(self.df):,} IT job records")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def basic_statistics(self):
        """Generate basic statistics about the dataset"""
        print("\n" + "="*60)
        print("BASIC DATASET STATISTICS")
        print("="*60)
        
        print(f"Total IT Job Postings: {len(self.df):,}")
        print(f"Date Range: {self.df['posting_date'].min()} to {self.df['posting_date'].max()}")
        print(f"Unique Companies: {self.df['company_id'].nunique():,}")
        print(f"Unique Job Titles: {self.df['title'].nunique():,}")
        
        # Check for missing data
        print(f"\nMissing Data Summary:")
        missing_data = self.df.isnull().sum()
        for col in missing_data[missing_data > 0].index:
            pct = (missing_data[col] / len(self.df)) * 100
            print(f"  - {col}: {missing_data[col]:,} ({pct:.1f}%)")
    
    def analyze_it_domains(self):
        """Analyze IT domain distribution and trends"""
        print("\n" + "="*60)
        print("IT DOMAIN ANALYSIS")
        print("="*60)
        
        # Domain distribution
        domain_counts = self.df['it_domain'].value_counts()
        print(f"\nIT Domain Distribution:")
        for domain, count in domain_counts.items():
            pct = (count / len(self.df)) * 100
            print(f"  - {domain}: {count:,} ({pct:.1f}%)")
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        domain_counts.plot(kind='bar', color='skyblue')
        plt.title('Distribution of IT Job Domains', fontsize=16, fontweight='bold')
        plt.xlabel('IT Domain', fontsize=12)
        plt.ylabel('Number of Job Postings', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{self.data_path.replace('.csv', '_domains.png')}", dpi=300, bbox_inches='tight')
        plt.show()
        
        return domain_counts
    
    def analyze_experience_levels(self):
        """Analyze experience level requirements"""
        print("\n" + "="*60)
        print("EXPERIENCE LEVEL ANALYSIS")
        print("="*60)
        
        exp_counts = self.df['experience_level'].value_counts()
        print(f"\nExperience Level Distribution:")
        for level, count in exp_counts.items():
            pct = (count / len(self.df)) * 100
            print(f"  - {level}: {count:,} ({pct:.1f}%)")
        
        # Experience by domain
        print(f"\nExperience Requirements by IT Domain:")
        domain_exp = pd.crosstab(self.df['it_domain'], self.df['experience_level'], normalize='index') * 100
        print(domain_exp.round(1))
        
        return exp_counts
    
    def analyze_work_types(self):
        """Analyze work type preferences"""
        print("\n" + "="*60)
        print("WORK TYPE ANALYSIS")
        print("="*60)
        
        work_counts = self.df['work_type'].value_counts()
        print(f"\nWork Type Distribution:")
        for work_type, count in work_counts.items():
            pct = (count / len(self.df)) * 100
            print(f"  - {work_type}: {count:,} ({pct:.1f}%)")
        
        # Remote work analysis
        remote_jobs = self.df['remote_allowed'].value_counts()
        print(f"\nRemote Work Options:")
        for option, count in remote_jobs.items():
            pct = (count / len(self.df)) * 100
            print(f"  - Remote Allowed ({option}): {count:,} ({pct:.1f}%)")
        
        return work_counts
    
    def analyze_companies(self):
        """Analyze company characteristics"""
        print("\n" + "="*60)
        print("COMPANY ANALYSIS")
        print("="*60)
        
        # Company size distribution
        size_counts = self.df['company_size'].value_counts()
        print(f"\nCompany Size Distribution:")
        for size, count in size_counts.items():
            pct = (count / len(self.df)) * 100
            print(f"  - {size}: {count:,} ({pct:.1f}%)")
        
        # Top hiring companies
        top_companies = self.df['company_name'].value_counts().head(10)
        print(f"\nTop 10 IT Hiring Companies:")
        for i, (company, count) in enumerate(top_companies.items(), 1):
            print(f"  {i:2d}. {company}: {count:,} job postings")
        
        return size_counts, top_companies
    
    def analyze_skills_demand(self):
        """Analyze in-demand skills"""
        print("\n" + "="*60)
        print("SKILLS DEMAND ANALYSIS")
        print("="*60)
        
        # Extract skills from job descriptions and titles
        all_skills = []
        
        # Common IT skills to look for
        skill_keywords = {
            'Python': ['python'],
            'Java': ['java'],
            'JavaScript': ['javascript', 'js'],
            'SQL': ['sql'],
            'AWS': ['aws', 'amazon web services'],
            'Docker': ['docker'],
            'Kubernetes': ['kubernetes', 'k8s'],
            'React': ['react'],
            'Angular': ['angular'],
            'Node.js': ['node.js', 'nodejs'],
            'Machine Learning': ['machine learning', 'ml'],
            'Artificial Intelligence': ['artificial intelligence', 'ai'],
            'Data Science': ['data science'],
            'Cloud Computing': ['cloud'],
            'DevOps': ['devops'],
            'Agile': ['agile', 'scrum'],
            'Git': ['git', 'github'],
            'Linux': ['linux'],
            'Azure': ['azure'],
            'TensorFlow': ['tensorflow'],
            'PyTorch': ['pytorch'],
            'Spark': ['spark'],
            'Hadoop': ['hadoop'],
            'Tableau': ['tableau'],
            'Power BI': ['power bi', 'powerbi'],
            'REST API': ['rest', 'api'],
            'MongoDB': ['mongodb'],
            'PostgreSQL': ['postgresql', 'postgres'],
            'MySQL': ['mysql'],
            'Redis': ['redis'],
            'Elasticsearch': ['elasticsearch'],
            'Jenkins': ['jenkins'],
            'Terraform': ['terraform'],
            'Ansible': ['ansible']
        }
        
        skill_counts = {}
        
        # Count skill mentions in job descriptions and titles
        for skill, keywords in skill_keywords.items():
            count = 0
            for keyword in keywords:
                # Search in title and description (case insensitive)
                title_matches = self.df['title'].str.contains(keyword, case=False, na=False).sum()
                desc_matches = self.df['description'].str.contains(keyword, case=False, na=False).sum()
                count += max(title_matches, desc_matches)  # Avoid double counting
            
            skill_counts[skill] = count
        
        # Sort skills by demand
        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\nTop 20 In-Demand IT Skills:")
        for i, (skill, count) in enumerate(sorted_skills[:20], 1):
            pct = (count / len(self.df)) * 100
            print(f"  {i:2d}. {skill}: {count:,} job postings ({pct:.1f}%)")
        
        # Create skills demand visualization
        top_skills = dict(sorted_skills[:15])
        plt.figure(figsize=(12, 8))
        plt.barh(list(top_skills.keys()), list(top_skills.values()), color='lightcoral')
        plt.title('Top 15 In-Demand IT Skills', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Job Postings', fontsize=12)
        plt.ylabel('Skills', fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{self.data_path.replace('.csv', '_skills.png')}", dpi=300, bbox_inches='tight')
        plt.show()
        
        return sorted_skills
    
    def analyze_salary_trends(self):
        """Analyze salary trends if data is available"""
        print("\n" + "="*60)
        print("SALARY ANALYSIS")
        print("="*60)
        
        if 'salary_yearly' in self.df.columns:
            salary_data = self.df['salary_yearly'].dropna()
            
            if len(salary_data) > 0:
                print(f"\nSalary Statistics (based on {len(salary_data):,} records):")
                print(f"  - Average: ${salary_data.mean():,.0f}")
                print(f"  - Median: ${salary_data.median():,.0f}")
                print(f"  - Standard Deviation: ${salary_data.std():,.0f}")
                print(f"  - Range: ${salary_data.min():,.0f} - ${salary_data.max():,.0f}")
                
                # Salary by domain
                salary_by_domain = self.df.groupby('it_domain')['salary_yearly'].agg(['mean', 'median', 'count']).round(0)
                salary_by_domain = salary_by_domain[salary_by_domain['count'] >= 10]  # At least 10 records
                salary_by_domain = salary_by_domain.sort_values('mean', ascending=False)
                
                print(f"\nAverage Salary by IT Domain (domains with ≥10 salary records):")
                for domain, row in salary_by_domain.iterrows():
                    print(f"  - {domain}: ${row['mean']:,.0f} (median: ${row['median']:,.0f}, n={row['count']:.0f})")
                
                return salary_data, salary_by_domain
            else:
                print("No salary data available in the dataset.")
                return None, None
        else:
            print("Salary column not found in the dataset.")
            return None, None
    
    def analyze_temporal_trends(self):
        """Analyze temporal trends in job postings"""
        print("\n" + "="*60)
        print("TEMPORAL TRENDS ANALYSIS")
        print("="*60)
        
        # Convert posting_date to datetime if not already
        self.df['posting_date'] = pd.to_datetime(self.df['posting_date'])
        
        # Monthly trends
        monthly_trends = self.df.groupby([self.df['posting_date'].dt.year, 
                                         self.df['posting_date'].dt.month]).size()
        
        print(f"\nJob Posting Trends by Month:")
        for (year, month), count in monthly_trends.tail(12).items():
            print(f"  - {year}-{month:02d}: {count:,} job postings")
        
        # Domain trends over time
        domain_trends = self.df.groupby([self.df['posting_date'].dt.to_period('M'), 
                                        'it_domain']).size().unstack(fill_value=0)
        
        if len(domain_trends) > 1:
            plt.figure(figsize=(14, 8))
            for domain in domain_trends.columns[:5]:  # Top 5 domains
                plt.plot(domain_trends.index.astype(str), domain_trends[domain], 
                        marker='o', label=domain, linewidth=2)
            
            plt.title('IT Job Posting Trends by Domain (Top 5)', fontsize=16, fontweight='bold')
            plt.xlabel('Month', fontsize=12)
            plt.ylabel('Number of Job Postings', fontsize=12)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{self.data_path.replace('.csv', '_trends.png')}", dpi=300, bbox_inches='tight')
            plt.show()
        
        return monthly_trends, domain_trends
    
    def generate_insights_report(self):
        """Generate key insights and recommendations"""
        print("\n" + "="*80)
        print("KEY INSIGHTS & MARKET PREDICTIONS")
        print("="*80)
        
        # Most marketable IT domains
        domain_counts = self.df['it_domain'].value_counts()
        top_domains = domain_counts.head(5)
        
        print(f"\n🎯 MOST MARKETABLE IT FIELDS (2025-2030):")
        for i, (domain, count) in enumerate(top_domains.items(), 1):
            pct = (count / len(self.df)) * 100
            print(f"  {i}. {domain} - {count:,} jobs ({pct:.1f}% of market)")
        
        # Experience level insights
        entry_level_pct = (self.df['experience_level'] == 'Entry level').sum() / len(self.df) * 100
        mid_senior_pct = (self.df['experience_level'] == 'Mid-Senior level').sum() / len(self.df) * 100
        
        print(f"\n💼 EXPERIENCE LEVEL OPPORTUNITIES:")
        print(f"  - Entry Level: {entry_level_pct:.1f}% of jobs (Good for new graduates)")
        print(f"  - Mid-Senior Level: {mid_senior_pct:.1f}% of jobs (High demand for experienced professionals)")
        
        # Remote work trends
        remote_pct = self.df['remote_allowed'].sum() / len(self.df) * 100
        print(f"\n🏠 REMOTE WORK OPPORTUNITIES:")
        print(f"  - {remote_pct:.1f}% of IT jobs offer remote work options")
        
        # Company size insights
        company_sizes = self.df['company_size'].value_counts()
        print(f"\n🏢 COMPANY SIZE DISTRIBUTION:")
        for size, count in company_sizes.items():
            pct = (count / len(self.df)) * 100
            print(f"  - {size} companies: {pct:.1f}% of opportunities")
        
        print(f"\n📈 STRATEGIC RECOMMENDATIONS:")
        print(f"  1. Focus on Data Science & Analytics skills - highest demand ({domain_counts.iloc[0]:,} jobs)")
        print(f"  2. Develop Software Development capabilities - strong market ({domain_counts.iloc[1]:,} jobs)")
        print(f"  3. Consider mid-senior level positions for better opportunities")
        print(f"  4. Look for remote-friendly positions to expand job market")
        print(f"  5. Target technology-focused companies for better IT career growth")
        
        print("\n" + "="*80)
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        if not self.load_data():
            return
        
        # Basic statistics
        self.basic_statistics()
        
        # Domain analysis
        domain_counts = self.analyze_it_domains()
        
        # Experience level analysis
        exp_counts = self.analyze_experience_levels()
        
        # Work type analysis
        work_counts = self.analyze_work_types()
        
        # Company analysis
        size_counts, top_companies = self.analyze_companies()
        
        # Skills demand analysis
        skills_demand = self.analyze_skills_demand()
        
        # Salary analysis
        salary_data, salary_by_domain = self.analyze_salary_trends()
        
        # Temporal trends
        monthly_trends, domain_trends = self.analyze_temporal_trends()
        
        # Generate insights
        self.generate_insights_report()
        
        print(f"\n✅ Analysis complete! Visualizations saved to {self.data_path.replace('.csv', '_*.png')}")

def main():
    """Main analysis execution"""
    print("Starting Comprehensive IT Job Market Analysis...")
    print("="*60)
    
    analyzer = ITJobAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
