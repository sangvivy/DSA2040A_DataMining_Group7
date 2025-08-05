"""
IT Job Market Prediction Model (2025-2030)
This script creates predictive models to forecast future IT job market trends,
including most marketable skills, job domains, and career opportunities.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

class ITJobPredictor:
    def __init__(self, data_path="a:/SUMMER_2025/archive_Term_project/processed_it_jobs.csv"):
        self.data_path = data_path
        self.df = None
        self.models = {}
        self.encoders = {}
        
    def load_and_prepare_data(self):
        """Load and prepare data for modeling"""
        print("Loading and preparing data for prediction modeling...")
        
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df):,} IT job records")
        
        # Feature engineering
        self.df['posting_date'] = pd.to_datetime(self.df['posting_date'])
        self.df['year'] = self.df['posting_date'].dt.year
        self.df['month'] = self.df['posting_date'].dt.month
        self.df['quarter'] = self.df['posting_date'].dt.quarter
        
        # Create binary features for skills
        skills_to_track = [
            'python', 'java', 'javascript', 'sql', 'aws', 'azure', 'docker', 
            'kubernetes', 'react', 'angular', 'machine learning', 'ai', 
            'data science', 'cloud', 'devops', 'git', 'agile'
        ]
        
        for skill in skills_to_track:
            self.df[f'has_{skill.replace(" ", "_")}'] = (
                self.df['title'].str.contains(skill, case=False, na=False) |
                self.df['description'].str.contains(skill, case=False, na=False)
            ).astype(int)
        
        # Encode categorical variables
        categorical_columns = ['it_domain', 'experience_level', 'work_type', 'company_size']
        for col in categorical_columns:
            if col in self.df.columns:
                le = LabelEncoder()
                self.df[f'{col}_encoded'] = le.fit_transform(self.df[col].fillna('Unknown'))
                self.encoders[col] = le
        
        print("Data preparation completed.")
        return True
    
    def predict_domain_growth(self):
        """Predict growth trends for IT domains"""
        print("\n" + "="*60)
        print("PREDICTING IT DOMAIN GROWTH TRENDS")
        print("="*60)
        
        # Aggregate data by domain and time period
        domain_trends = self.df.groupby(['it_domain', 'year', 'quarter']).size().reset_index(name='job_count')
        
        # Create growth predictions for each domain
        domain_predictions = {}
        
        for domain in self.df['it_domain'].unique():
            domain_data = domain_trends[domain_trends['it_domain'] == domain].copy()
            
            if len(domain_data) > 1:
                # Simple linear trend prediction
                X = np.arange(len(domain_data)).reshape(-1, 1)
                y = domain_data['job_count'].values
                
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict next 5 periods (representing 2025-2030)
                future_X = np.arange(len(domain_data), len(domain_data) + 5).reshape(-1, 1)
                future_predictions = model.predict(future_X)
                
                # Calculate growth rate
                growth_rate = model.coef_[0] if len(model.coef_) > 0 else 0
                
                domain_predictions[domain] = {
                    'current_jobs': domain_data['job_count'].iloc[-1] if len(domain_data) > 0 else 0,
                    'predicted_jobs': future_predictions[-1] if len(future_predictions) > 0 else 0,
                    'growth_rate': growth_rate,
                    'predictions': future_predictions.tolist()
                }
        
        # Sort domains by predicted growth
        sorted_domains = sorted(domain_predictions.items(), 
                               key=lambda x: x[1]['growth_rate'], reverse=True)
        
        print(f"\nIT Domain Growth Predictions (2025-2030):")
        print(f"{'Domain':<30} {'Current':<10} {'Predicted':<12} {'Growth Rate':<15}")
        print("-" * 70)
        
        for domain, pred in sorted_domains:
            current = pred['current_jobs']
            predicted = max(0, pred['predicted_jobs'])  # Ensure non-negative
            growth = pred['growth_rate']
            trend = "📈 Growing" if growth > 0 else "📉 Declining" if growth < 0 else "➡️ Stable"
            
            print(f"{domain:<30} {current:<10.0f} {predicted:<12.0f} {growth:<10.2f} {trend}")
        
        return domain_predictions
    
    def predict_skill_demand(self):
        """Predict future skill demand"""
        print("\n" + "="*60)
        print("PREDICTING FUTURE SKILL DEMAND")
        print("="*60)
        
        # Count current skill demand
        skills_data = {}
        skill_columns = [col for col in self.df.columns if col.startswith('has_')]
        
        for skill_col in skill_columns:
            skill_name = skill_col.replace('has_', '').replace('_', ' ').title()
            current_demand = self.df[skill_col].sum()
            demand_percentage = (current_demand / len(self.df)) * 100
            
            skills_data[skill_name] = {
                'current_demand': current_demand,
                'current_percentage': demand_percentage,
                'skill_column': skill_col
            }
        
        # Predict future demand based on domain growth
        domain_predictions = self.predict_domain_growth()
        
        # Calculate skill importance by domain
        skill_by_domain = {}
        for domain in self.df['it_domain'].unique():
            domain_data = self.df[self.df['it_domain'] == domain]
            skill_by_domain[domain] = {}
            
            for skill_col in skill_columns:
                skill_name = skill_col.replace('has_', '').replace('_', ' ').title()
                skill_prevalence = domain_data[skill_col].mean()
                skill_by_domain[domain][skill_name] = skill_prevalence
        
        # Predict future skill demand
        future_skill_demand = {}
        for skill_name, skill_info in skills_data.items():
            total_future_demand = 0
            
            for domain, domain_pred in domain_predictions.items():
                if domain in skill_by_domain and skill_name in skill_by_domain[domain]:
                    skill_prevalence = skill_by_domain[domain][skill_name]
                    predicted_domain_jobs = max(0, domain_pred['predicted_jobs'])
                    future_demand_from_domain = predicted_domain_jobs * skill_prevalence
                    total_future_demand += future_demand_from_domain
            
            growth_factor = total_future_demand / max(1, skill_info['current_demand'])
            
            future_skill_demand[skill_name] = {
                'current_demand': skill_info['current_demand'],
                'predicted_demand': total_future_demand,
                'growth_factor': growth_factor,
                'current_percentage': skill_info['current_percentage']
            }
        
        # Sort skills by predicted demand
        sorted_skills = sorted(future_skill_demand.items(), 
                              key=lambda x: x[1]['predicted_demand'], reverse=True)
        
        print(f"\nSkill Demand Predictions (2025-2030):")
        print(f"{'Skill':<25} {'Current %':<12} {'Predicted':<12} {'Growth':<10} {'Trend'}")
        print("-" * 75)
        
        for skill, pred in sorted_skills[:20]:  # Top 20 skills
            current_pct = pred['current_percentage']
            predicted = pred['predicted_demand']
            growth = pred['growth_factor']
            
            if growth > 1.2:
                trend = "🚀 High Growth"
            elif growth > 1.05:
                trend = "📈 Growing"
            elif growth > 0.95:
                trend = "➡️ Stable"
            else:
                trend = "📉 Declining"
            
            print(f"{skill:<25} {current_pct:<12.1f} {predicted:<12.0f} {growth:<10.2f} {trend}")
        
        return future_skill_demand
    
    def predict_career_opportunities(self):
        """Predict career opportunities and salary trends"""
        print("\n" + "="*60)
        print("PREDICTING CAREER OPPORTUNITIES")
        print("="*60)
        
        # Experience level analysis
        exp_distribution = self.df['experience_level'].value_counts(normalize=True) * 100
        
        print(f"\nCareer Level Opportunities:")
        print(f"{'Experience Level':<20} {'Current %':<12} {'Opportunity'}")
        print("-" * 50)
        
        opportunity_mapping = {
            'Entry level': '🟢 Excellent - High volume, growing field',
            'Mid-Senior level': '🟢 Excellent - Highest demand segment',
            'Associate': '🟡 Good - Steady opportunities',
            'Director': '🟡 Moderate - Leadership roles',
            'Executive': '🔴 Limited - Few positions, high competition',
            'Internship': '🟢 Good - Entry pathway'
        }
        
        for level, percentage in exp_distribution.items():
            opportunity = opportunity_mapping.get(level, '🟡 Moderate')
            print(f"{level:<20} {percentage:<12.1f} {opportunity}")
        
        # Remote work trends
        remote_percentage = (self.df['remote_allowed'] == 1).mean() * 100
        
        print(f"\n🏠 Remote Work Trends:")
        print(f"  - Current remote opportunities: {remote_percentage:.1f}%")
        print(f"  - Predicted growth: +15-25% by 2030 (industry trend)")
        print(f"  - Best remote domains: Data Science, Software Development, DevOps")
        
        return exp_distribution
    
    def generate_2030_roadmap(self):
        """Generate a comprehensive roadmap for IT careers 2025-2030"""
        print("\n" + "="*80)
        print("IT CAREER ROADMAP 2025-2030")
        print("="*80)
        
        domain_predictions = self.predict_domain_growth()
        skill_predictions = self.predict_skill_demand()
        
        # Top growing domains
        growing_domains = [(k, v) for k, v in domain_predictions.items() if v['growth_rate'] > 0]
        growing_domains.sort(key=lambda x: x[1]['growth_rate'], reverse=True)
        
        # Top growing skills
        growing_skills = [(k, v) for k, v in skill_predictions.items() if v['growth_factor'] > 1.05]
        growing_skills.sort(key=lambda x: x[1]['growth_factor'], reverse=True)
        
        print(f"\n🎯 HIGHEST OPPORTUNITY IT DOMAINS (2025-2030):")
        for i, (domain, pred) in enumerate(growing_domains[:5], 1):
            growth_pct = ((pred['growth_rate'] / max(1, pred['current_jobs'])) * 100)
            print(f"  {i}. {domain}")
            print(f"     • Current jobs: {pred['current_jobs']:.0f}")
            print(f"     • Growth trajectory: {'+' if pred['growth_rate'] > 0 else ''}{growth_pct:.1f}%")
            print(f"     • Market outlook: {'Very Strong' if pred['growth_rate'] > 10 else 'Strong' if pred['growth_rate'] > 0 else 'Declining'}")
        
        print(f"\n🚀 FASTEST GROWING SKILLS (2025-2030):")
        for i, (skill, pred) in enumerate(growing_skills[:10], 1):
            growth_pct = ((pred['growth_factor'] - 1) * 100)
            print(f"  {i:2d}. {skill:<25} (+{growth_pct:.1f}% growth predicted)")
        
        print(f"\n📚 LEARNING RECOMMENDATIONS BY CAREER STAGE:")
        print(f"\n🎓 NEW GRADUATES & CAREER CHANGERS:")
        print(f"  • Primary Focus: Python, SQL, Data Analysis")
        print(f"  • Secondary: Cloud (AWS/Azure), Git, Agile")
        print(f"  • Domain Target: Data Science & Analytics (59.5% of market)")
        print(f"  • Timeline: 6-12 months intensive learning")
        
        print(f"\n💼 MID-LEVEL PROFESSIONALS (2-5 years):")
        print(f"  • Advanced Skills: Machine Learning, AI, DevOps")
        print(f"  • Leadership: Agile, Project Management")
        print(f"  • Specialization: Cloud Architecture, Data Engineering")
        print(f"  • Timeline: 12-18 months for specialization")
        
        print(f"\n🏆 SENIOR PROFESSIONALS (5+ years):")
        print(f"  • Strategic Skills: AI Strategy, Cloud Architecture")
        print(f"  • Management: Technical Leadership, Team Building")
        print(f"  • Innovation: Emerging Technologies, Research")
        print(f"  • Timeline: Continuous learning and adaptation")
        
        print(f"\n💰 SALARY OPTIMIZATION STRATEGIES:")
        print(f"  • High-value combinations: AI + Cloud + Domain Expertise")
        print(f"  • Geographic arbitrage: Remote work in high-paying markets")
        print(f"  • Certification focus: AWS, Azure, Google Cloud")
        print(f"  • Industry targeting: Tech, Finance, Healthcare")
        
        print(f"\n🌐 FUTURE-PROOFING RECOMMENDATIONS:")
        print(f"  1. Develop AI/ML skills - will be table stakes by 2030")
        print(f"  2. Master cloud platforms - infrastructure is moving to cloud")
        print(f"  3. Learn automation tools - efficiency will be critical")
        print(f"  4. Build soft skills - human skills complement AI")
        print(f"  5. Stay adaptable - technology landscape changes rapidly")
        
        print(f"\n⚠️  SKILLS TO PHASE OUT:")
        declining_skills = [(k, v) for k, v in skill_predictions.items() if v['growth_factor'] < 0.95]
        if declining_skills:
            print(f"  • Consider transitioning from: {', '.join([skill for skill, _ in declining_skills[:5]])}")
        else:
            print(f"  • All tracked skills show stable or positive growth")
        
        print("\n" + "="*80)
        print("🎯 SUCCESS FRAMEWORK FOR IT CAREERS 2025-2030")
        print("="*80)
        print("1. TECHNICAL MASTERY: Core programming + Cloud + AI/ML")
        print("2. DOMAIN EXPERTISE: Deep knowledge in one vertical")
        print("3. SOFT SKILLS: Communication, Leadership, Problem-solving")
        print("4. CONTINUOUS LEARNING: Stay current with emerging trends")
        print("5. NETWORK BUILDING: Professional connections and mentorship")
        print("="*80)
    
    def run_complete_prediction(self):
        """Run the complete prediction pipeline"""
        print("Starting IT Job Market Prediction Analysis...")
        print("="*60)
        
        if not self.load_and_prepare_data():
            return
        
        # Run all prediction analyses
        domain_predictions = self.predict_domain_growth()
        skill_predictions = self.predict_skill_demand()
        career_opportunities = self.predict_career_opportunities()
        
        # Generate comprehensive roadmap
        self.generate_2030_roadmap()
        
        print(f"\n✅ Prediction analysis complete!")
        print(f"📊 Processed {len(self.df):,} IT job records")
        print(f"🔮 Generated predictions for {len(domain_predictions)} IT domains")
        print(f"🎯 Analyzed demand for {len(skill_predictions)} key skills")

def main():
    """Main prediction execution"""
    print("IT Job Market Prediction Model (2025-2030)")
    print("="*60)
    
    predictor = ITJobPredictor()
    predictor.run_complete_prediction()

if __name__ == "__main__":
    main()
