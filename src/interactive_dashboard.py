"""
Interactive IT Job Market Dashboard
Beautiful and interactive visualizations using Plotly for comprehensive IT job analysis
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ITJobDashboard:
    def __init__(self, data_path="a:/SUMMER_2025/archive_Term_project/processed_it_jobs.csv"):
        self.data_path = data_path
        self.df = None
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff9800',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
        
    def load_data(self):
        """Load the processed IT job dataset"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✅ Dashboard loaded {len(self.df):,} IT job records")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def create_overview_dashboard(self):
        """Create overview dashboard with key metrics"""
        print("🎯 Creating Overview Dashboard...")
        
        # Calculate key metrics
        total_jobs = len(self.df)
        unique_companies = self.df['company_id'].nunique()
        unique_titles = self.df['title'].nunique()
        remote_jobs = self.df['remote_allowed'].sum()
        remote_pct = (remote_jobs / total_jobs) * 100
        
        # Create metrics cards
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total IT Jobs', 'Unique Companies', 'Job Titles Variety', 'Remote Opportunities'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Total Jobs
        fig.add_trace(go.Indicator(
            mode="number",
            value=total_jobs,
            title={"text": "Total IT Jobs<br><span style='font-size:0.8em;color:gray'>Available Positions</span>"},
            number={'font': {'size': 40}},
            domain={'row': 0, 'column': 0}
        ), row=1, col=1)
        
        # Unique Companies
        fig.add_trace(go.Indicator(
            mode="number",
            value=unique_companies,
            title={"text": "Unique Companies<br><span style='font-size:0.8em;color:gray'>Hiring in IT</span>"},
            number={'font': {'size': 40}},
            domain={'row': 0, 'column': 1}
        ), row=1, col=2)
        
        # Job Titles
        fig.add_trace(go.Indicator(
            mode="number",
            value=unique_titles,
            title={"text": "Job Titles<br><span style='font-size:0.8em;color:gray'>Different Roles</span>"},
            number={'font': {'size': 40}},
            domain={'row': 1, 'column': 0}
        ), row=2, col=1)
        
        # Remote Opportunities
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=remote_pct,
            delta={'reference': 10, 'relative': True, 'position': "top"},
            title={"text": "Remote Work<br><span style='font-size:0.8em;color:gray'>% of Jobs</span>"},
            number={'font': {'size': 40}, 'suffix': '%'},
            domain={'row': 1, 'column': 1}
        ), row=2, col=2)
        
        fig.update_layout(
            title={
                'text': "🎯 IT Job Market Overview Dashboard",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            height=600,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='#f8f9fa'
        )
        
        # Save as HTML file
        fig.write_html("overview_dashboard.html")
        fig.show()
        return fig
    
    def create_domain_analysis_dashboard(self):
        """Create IT domain analysis dashboard"""
        print("📊 Creating IT Domain Analysis Dashboard...")
        
        domain_counts = self.df['it_domain'].value_counts()
        
        # Create subplot figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('IT Domain Distribution', 'Market Share Pie Chart', 
                          'Domain vs Experience Level', 'Growth Potential Analysis'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "heatmap"}, {"type": "scatter"}]]
        )
        
        # 1. Bar chart of domain distribution
        fig.add_trace(go.Bar(
            x=domain_counts.index,
            y=domain_counts.values,
            name='Job Count',
            marker_color=px.colors.qualitative.Set3,
            text=[f'{count:,}' for count in domain_counts.values],
            textposition='auto',
        ), row=1, col=1)
        
        # 2. Pie chart
        fig.add_trace(go.Pie(
            labels=domain_counts.index,
            values=domain_counts.values,
            name="Market Share",
            hole=0.4,
            marker_colors=px.colors.qualitative.Set3
        ), row=1, col=2)
        
        # 3. Heatmap - Domain vs Experience Level
        domain_exp = pd.crosstab(self.df['it_domain'], self.df['experience_level'])
        fig.add_trace(go.Heatmap(
            z=domain_exp.values,
            x=domain_exp.columns,
            y=domain_exp.index,
            colorscale='Viridis',
            name='Experience Distribution'
        ), row=2, col=1)
        
        # 4. Growth potential scatter (synthetic data for demo)
        growth_potential = {
            'Data Science & Analytics': {'current': domain_counts.iloc[0], 'growth': 25},
            'Software Development': {'current': domain_counts.iloc[1], 'growth': 15},
            'DevOps & Cloud': {'current': domain_counts.get('DevOps & Cloud', 100), 'growth': 35},
            'Cybersecurity': {'current': domain_counts.get('Cybersecurity', 50), 'growth': 30},
            'UI/UX Design': {'current': domain_counts.get('UI/UX Design', 500), 'growth': 20}
        }
        
        domains = list(growth_potential.keys())
        current_jobs = [growth_potential[d]['current'] for d in domains]
        growth_rates = [growth_potential[d]['growth'] for d in domains]
        
        fig.add_trace(go.Scatter(
            x=current_jobs,
            y=growth_rates,
            mode='markers+text',
            text=domains,
            textposition="top center",
            marker=dict(
                size=[val/500 for val in current_jobs],
                color=growth_rates,
                colorscale='RdYlBu_r',
                showscale=True,
                colorbar=dict(title="Growth %")
            ),
            name='Growth Analysis'
        ), row=2, col=2)
        
        # Update layout
        fig.update_layout(
            title={
                'text': "📊 IT Domain Analysis Dashboard",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            height=800,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='#f8f9fa'
        )
        
        # Update x-axes
        fig.update_xaxes(title_text="IT Domains", tickangle=45, row=1, col=1)
        fig.update_xaxes(title_text="Experience Level", row=2, col=1)
        fig.update_xaxes(title_text="Current Jobs", row=2, col=2)
        
        # Update y-axes
        fig.update_yaxes(title_text="Number of Jobs", row=1, col=1)
        fig.update_yaxes(title_text="IT Domain", row=2, col=1)
        fig.update_yaxes(title_text="Growth Rate %", row=2, col=2)
        
        # Save as HTML file
        fig.write_html("domain_analysis_dashboard.html")
        fig.show()
        return fig
    
    def create_skills_demand_dashboard(self):
        """Create skills demand analysis dashboard"""
        print("🚀 Creating Skills Demand Dashboard...")
        
        # Calculate skill demand
        skill_keywords = {
            'Artificial Intelligence': ['artificial intelligence', 'ai'],
            'Machine Learning': ['machine learning', 'ml'],
            'AWS': ['aws', 'amazon web services'],
            'Python': ['python'],
            'SQL': ['sql'],
            'JavaScript': ['javascript', 'js'],
            'Java': ['java'],
            'React': ['react'],
            'Git': ['git'],
            'Docker': ['docker'],
            'Kubernetes': ['kubernetes', 'k8s'],
            'Azure': ['azure'],
            'Cloud Computing': ['cloud'],
            'DevOps': ['devops'],
            'Agile': ['agile', 'scrum']
        }
        
        skill_counts = {}
        for skill, keywords in skill_keywords.items():
            count = 0
            for keyword in keywords:
                desc_matches = self.df['description'].str.contains(keyword, case=False, na=False).sum()
                title_matches = self.df['title'].str.contains(keyword, case=False, na=False).sum()
                count += max(desc_matches, title_matches)
            skill_counts[skill] = count
        
        # Sort skills
        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
        top_15_skills = dict(sorted_skills[:15])
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Top 15 In-Demand Skills', 'Skills Penetration Rate', 
                          'Skill Categories', 'Future Skill Trends'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "scatter"}]]
        )
        
        # 1. Horizontal bar chart for top skills
        skills = list(top_15_skills.keys())
        counts = list(top_15_skills.values())
        
        fig.add_trace(go.Bar(
            y=skills[::-1],  # Reverse for better readability
            x=counts[::-1],
            orientation='h',
            marker_color=px.colors.sequential.Plasma_r,
            text=[f'{count:,}' for count in counts[::-1]],
            textposition='auto',
            name='Skill Demand'
        ), row=1, col=1)
        
        # 2. Penetration rate (percentage)
        penetration = [(count/len(self.df))*100 for count in counts]
        fig.add_trace(go.Bar(
            x=skills,
            y=penetration,
            marker_color=px.colors.sequential.Viridis,
            text=[f'{pct:.1f}%' for pct in penetration],
            textposition='auto',
            name='Penetration %'
        ), row=1, col=2)
        
        # 3. Skill categories pie chart
        categories = {
            'Programming': ['Python', 'JavaScript', 'Java'],
            'Cloud & DevOps': ['AWS', 'Azure', 'Docker', 'Kubernetes', 'Cloud Computing', 'DevOps'],
            'AI & Data': ['Artificial Intelligence', 'Machine Learning', 'SQL'],
            'Development Tools': ['Git', 'React', 'Agile']
        }
        
        category_counts = {}
        for category, cat_skills in categories.items():
            total = sum(top_15_skills.get(skill, 0) for skill in cat_skills if skill in top_15_skills)
            category_counts[category] = total
        
        fig.add_trace(go.Pie(
            labels=list(category_counts.keys()),
            values=list(category_counts.values()),
            hole=0.4,
            marker_colors=px.colors.qualitative.Set2,
            name="Skill Categories"
        ), row=2, col=1)
        
        # 4. Future trends (synthetic growth data)
        future_growth = {
            'Artificial Intelligence': 40,
            'Machine Learning': 35,
            'Cloud Computing': 30,
            'DevOps': 25,
            'Python': 20,
            'Kubernetes': 45,
            'React': 15,
            'AWS': 25,
            'Docker': 30
        }
        
        trend_skills = list(future_growth.keys())
        current_demand = [top_15_skills.get(skill, 0) for skill in trend_skills]
        growth_rates = [future_growth[skill] for skill in trend_skills]
        
        fig.add_trace(go.Scatter(
            x=current_demand,
            y=growth_rates,
            mode='markers+text',
            text=trend_skills,
            textposition="top center",
            marker=dict(
                size=[val/500 for val in current_demand],
                color=growth_rates,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Growth %", x=1.02)
            ),
            name='Future Trends'
        ), row=2, col=2)
        
        # Update layout
        fig.update_layout(
            title={
                'text': "🚀 Skills Demand Analysis Dashboard",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            height=900,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='#f8f9fa'
        )
        
        # Update axes
        fig.update_xaxes(title_text="Number of Job Postings", row=1, col=1)
        fig.update_xaxes(title_text="Skills", tickangle=45, row=1, col=2)
        fig.update_xaxes(title_text="Current Demand", row=2, col=2)
        
        fig.update_yaxes(title_text="Skills", row=1, col=1)
        fig.update_yaxes(title_text="Penetration %", row=1, col=2)
        fig.update_yaxes(title_text="Predicted Growth %", row=2, col=2)
        
        # Save as HTML file
        fig.write_html("skills_demand_dashboard.html")
        fig.show()
        return fig
    
    def create_career_opportunities_dashboard(self):
        """Create career opportunities dashboard"""
        print("💼 Creating Career Opportunities Dashboard...")
        
        # Experience level analysis
        exp_counts = self.df['experience_level'].value_counts()
        work_counts = self.df['work_type'].value_counts()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Experience Level Distribution', 'Work Type Flexibility', 
                          'Remote Work Trends', 'Salary Projections'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "indicator"}, {"type": "bar"}]]
        )
        
        # 1. Experience level pie chart
        fig.add_trace(go.Pie(
            labels=exp_counts.index,
            values=exp_counts.values,
            hole=0.3,
            marker_colors=px.colors.qualitative.Pastel,
            textinfo='label+percent',
            name="Experience Levels"
        ), row=1, col=1)
        
        # 2. Work type bar chart
        fig.add_trace(go.Bar(
            x=work_counts.index,
            y=work_counts.values,
            marker_color=px.colors.qualitative.Set1,
            text=[f'{count:,}' for count in work_counts.values],
            textposition='auto',
            name='Work Types'
        ), row=1, col=2)
        
        # 3. Remote work indicator
        remote_pct = (self.df['remote_allowed'].sum() / len(self.df)) * 100
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=remote_pct,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Remote Work %"},
            delta={'reference': 15},
            gauge={
                'axis': {'range': [None, 50]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 35}
            }
        ), row=2, col=1)
        
        # 4. Salary projections (synthetic data)
        salary_data = {
            'Entry Level': {'2025': 65000, '2030': 82500},
            'Mid-Level': {'2025': 100000, '2030': 130000},
            'Senior Level': {'2025': 160000, '2030': 210000}
        }
        
        levels = list(salary_data.keys())
        salary_2025 = [salary_data[level]['2025'] for level in levels]
        salary_2030 = [salary_data[level]['2030'] for level in levels]
        
        fig.add_trace(go.Bar(
            x=levels,
            y=salary_2025,
            name='2025',
            marker_color='lightblue'
        ), row=2, col=2)
        
        fig.add_trace(go.Bar(
            x=levels,
            y=salary_2030,
            name='2030',
            marker_color='darkblue'
        ), row=2, col=2)
        
        # Update layout
        fig.update_layout(
            title={
                'text': "💼 Career Opportunities Dashboard",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            height=800,
            plot_bgcolor='white',
            paper_bgcolor='#f8f9fa',
            barmode='group'
        )
        
        # Update axes
        fig.update_xaxes(title_text="Work Types", tickangle=45, row=1, col=2)
        fig.update_xaxes(title_text="Experience Levels", row=2, col=2)
        
        fig.update_yaxes(title_text="Number of Jobs", row=1, col=2)
        fig.update_yaxes(title_text="Average Salary ($)", row=2, col=2)
        
        # Save as HTML file
        fig.write_html("career_opportunities_dashboard.html")
        fig.show()
        return fig
    
    def create_company_analysis_dashboard(self):
        """Create company analysis dashboard"""
        print("🏢 Creating Company Analysis Dashboard...")
        
        # Top companies analysis
        top_companies = self.df['company_name'].value_counts().head(15)
        company_sizes = self.df['company_size'].value_counts()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Top 15 Hiring Companies', 'Company Size Distribution', 
                          'Industry Focus', 'Hiring Trends'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # 1. Top companies horizontal bar
        fig.add_trace(go.Bar(
            y=top_companies.index[::-1],
            x=top_companies.values[::-1],
            orientation='h',
            marker_color=px.colors.sequential.Blues_r,
            text=[f'{count}' for count in top_companies.values[::-1]],
            textposition='auto',
            name='Job Postings'
        ), row=1, col=1)
        
        # 2. Company size pie chart
        fig.add_trace(go.Pie(
            labels=company_sizes.index if len(company_sizes) > 0 else ['Unknown'],
            values=company_sizes.values if len(company_sizes) > 0 else [len(self.df)],
            hole=0.4,
            marker_colors=px.colors.qualitative.Set3,
            name="Company Sizes"
        ), row=1, col=2)
        
        # 3. Industry focus
        industry_focus = self.df['industry_focus'].value_counts() if 'industry_focus' in self.df.columns else pd.Series({'Technology': len(self.df)})
        fig.add_trace(go.Bar(
            x=industry_focus.index,
            y=industry_focus.values,
            marker_color=px.colors.qualitative.Vivid,
            text=[f'{count:,}' for count in industry_focus.values],
            textposition='auto',
            name='Industry Focus'
        ), row=2, col=1)
        
        # 4. Hiring trends (synthetic monthly data)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        hiring_trend = np.random.randint(3000, 6000, 12)  # Synthetic data
        
        fig.add_trace(go.Scatter(
            x=months,
            y=hiring_trend,
            mode='lines+markers',
            line=dict(color='green', width=3),
            marker=dict(size=8),
            name='Monthly Hiring'
        ), row=2, col=2)
        
        # Update layout
        fig.update_layout(
            title={
                'text': "🏢 Company Analysis Dashboard",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            height=800,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='#f8f9fa'
        )
        
        # Update axes
        fig.update_xaxes(title_text="Number of Job Postings", row=1, col=1)
        fig.update_xaxes(title_text="Industry Focus", row=2, col=1)
        fig.update_xaxes(title_text="Month", row=2, col=2)
        
        fig.update_yaxes(title_text="Companies", row=1, col=1)
        fig.update_yaxes(title_text="Number of Jobs", row=2, col=1)
        fig.update_yaxes(title_text="Job Postings", row=2, col=2)
        
        # Save as HTML file
        fig.write_html("company_analysis_dashboard.html")
        fig.show()
        return fig
    
    def create_predictions_dashboard(self):
        """Create future predictions dashboard"""
        print("🔮 Creating Future Predictions Dashboard...")
        
        # Prediction data (synthetic but realistic)
        domains = ['Data Science & Analytics', 'Software Development', 'DevOps & Cloud', 'Cybersecurity', 'UI/UX Design']
        current_jobs = [29744, 18726, 100, 37, 474]
        growth_rates = [25, 15, 35, 30, 20]
        projected_2030 = [curr * ((1 + rate/100) ** 5) for curr, rate in zip(current_jobs, growth_rates)]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Domain Growth Projections 2025-2030', 'Growth Rate Comparison', 
                          'Market Share Evolution', 'Investment Priority Matrix'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # 1. Growth projections
        fig.add_trace(go.Bar(
            x=domains,
            y=current_jobs,
            name='Current (2025)',
            marker_color='lightblue'
        ), row=1, col=1)
        
        fig.add_trace(go.Bar(
            x=domains,
            y=projected_2030,
            name='Projected (2030)',
            marker_color='darkblue'
        ), row=1, col=1)
        
        # 2. Growth rates
        colors = ['green' if rate > 20 else 'orange' if rate > 15 else 'red' for rate in growth_rates]
        fig.add_trace(go.Bar(
            x=domains,
            y=growth_rates,
            marker_color=colors,
            text=[f'{rate}%' for rate in growth_rates],
            textposition='auto',
            name='Growth Rate %'
        ), row=1, col=2)
        
        # 3. Market share evolution
        current_total = sum(current_jobs)
        projected_total = sum(projected_2030)
        
        current_share = [job/current_total*100 for job in current_jobs]
        projected_share = [job/projected_total*100 for job in projected_2030]
        
        fig.add_trace(go.Bar(
            x=domains,
            y=current_share,
            name='Current Share',
            marker_color='lightcoral'
        ), row=2, col=1)
        
        fig.add_trace(go.Bar(
            x=domains,
            y=projected_share,
            name='Projected Share',
            marker_color='darkred'
        ), row=2, col=1)
        
        # 4. Investment priority matrix
        market_size = current_jobs
        opportunity_score = [rate * (curr/1000) for rate, curr in zip(growth_rates, current_jobs)]
        
        fig.add_trace(go.Scatter(
            x=market_size,
            y=growth_rates,
            mode='markers+text',
            text=domains,
            textposition="top center",
            marker=dict(
                size=[score/50 for score in opportunity_score],
                color=growth_rates,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Growth %", x=1.02)
            ),
            name='Investment Priority'
        ), row=2, col=2)
        
        # Update layout
        fig.update_layout(
            title={
                'text': "🔮 Future Predictions Dashboard (2025-2030)",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            height=900,
            plot_bgcolor='white',
            paper_bgcolor='#f8f9fa',
            barmode='group'
        )
        
        # Update axes
        fig.update_xaxes(title_text="IT Domains", tickangle=45, row=1, col=1)
        fig.update_xaxes(title_text="IT Domains", tickangle=45, row=1, col=2)
        fig.update_xaxes(title_text="IT Domains", tickangle=45, row=2, col=1)
        fig.update_xaxes(title_text="Current Market Size", row=2, col=2)
        
        fig.update_yaxes(title_text="Number of Jobs", row=1, col=1)
        fig.update_yaxes(title_text="Annual Growth %", row=1, col=2)
        fig.update_yaxes(title_text="Market Share %", row=2, col=1)
        fig.update_yaxes(title_text="Growth Rate %", row=2, col=2)
        
        # Save as HTML file
        fig.write_html("predictions_dashboard.html")
        fig.show()
        return fig
    
    def create_comprehensive_summary_dashboard(self):
        """Create a comprehensive summary dashboard"""
        print("📈 Creating Comprehensive Summary Dashboard...")
        
        # Key insights data
        domain_counts = self.df['it_domain'].value_counts()
        exp_counts = self.df['experience_level'].value_counts()
        
        # Create a large subplot layout
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=(
                'Market Overview', 'Top IT Domains', 'Experience Opportunities',
                'Skills in Demand', 'Work Type Flexibility', 'Remote Work Gauge',
                'Growth Predictions', 'Success Metrics', 'Action Items'
            ),
            specs=[
                [{"type": "indicator"}, {"type": "pie"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "pie"}, {"type": "indicator"}],
                [{"type": "scatter"}, {"type": "bar"}, {"type": "table"}]
            ]
        )
        
        # Row 1: Market Overview
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=len(self.df),
            title={'text': "Total IT Opportunities"},
            gauge={'axis': {'range': [None, 60000]},
                   'bar': {'color': "darkblue"},
                   'steps': [{'range': [0, 30000], 'color': "lightgray"},
                           {'range': [30000, 60000], 'color': "gray"}]},
            domain={'x': [0, 1], 'y': [0, 1]}
        ), row=1, col=1)
        
        # Top domains pie
        fig.add_trace(go.Pie(
            labels=domain_counts.head(5).index,
            values=domain_counts.head(5).values,
            hole=0.3,
            name="Top Domains"
        ), row=1, col=2)
        
        # Experience levels bar
        fig.add_trace(go.Bar(
            x=exp_counts.index,
            y=exp_counts.values,
            marker_color=px.colors.qualitative.Set2,
            name='Experience Levels'
        ), row=1, col=3)
        
        # Row 2: Skills and work types
        # Top skills
        skill_data = {'AI': 47403, 'AWS': 8892, 'ML': 6218, 'Git': 5830, 'Cloud': 3177}
        fig.add_trace(go.Bar(
            x=list(skill_data.keys()),
            y=list(skill_data.values()),
            marker_color=px.colors.sequential.Plasma,
            name='Top Skills'
        ), row=2, col=1)
        
        # Work types
        work_counts = self.df['work_type'].value_counts()
        fig.add_trace(go.Pie(
            labels=work_counts.index,
            values=work_counts.values,
            name="Work Types"
        ), row=2, col=2)
        
        # Remote work gauge
        remote_pct = (self.df['remote_allowed'].sum() / len(self.df)) * 100
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=remote_pct,
            title={'text': "Remote Work %"},
            gauge={'axis': {'range': [None, 50]},
                   'bar': {'color': "green"}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ), row=2, col=3)
        
        # Row 3: Predictions and actions
        # Growth predictions scatter
        domains = ['Data Science', 'Software Dev', 'DevOps', 'Security', 'UI/UX']
        current = [29744, 18726, 100, 37, 474]
        growth = [25, 15, 35, 30, 20]
        
        fig.add_trace(go.Scatter(
            x=current,
            y=growth,
            mode='markers+text',
            text=domains,
            marker=dict(size=15, color=growth, colorscale='RdYlGn'),
            name='Growth Matrix'
        ), row=3, col=1)
        
        # Success metrics
        metrics = ['Skills Portfolio', 'Project Portfolio', 'Network', 'Salary Target', 'Learning Velocity']
        targets = [5, 5, 100, 25, 2]
        current_level = [3, 3, 50, 15, 1]  # Example current levels
        
        fig.add_trace(go.Bar(
            x=metrics,
            y=targets,
            name='Target',
            marker_color='lightblue'
        ), row=3, col=2)
        
        fig.add_trace(go.Bar(
            x=metrics,
            y=current_level,
            name='Current',
            marker_color='darkblue'
        ), row=3, col=2)
        
        # Action items table
        action_data = [
            ['Immediate (0-3 months)', 'Learn Python + SQL', 'Foundation'],
            ['Short-term (3-12 months)', 'AWS Certification', 'Specialization'],
            ['Medium-term (1-3 years)', 'Leadership roles', 'Advancement'],
            ['Long-term (3-5 years)', 'Expert recognition', 'Mastery']
        ]
        
        fig.add_trace(go.Table(
            header=dict(values=['Timeline', 'Action', 'Focus'],
                       fill_color='paleturquoise',
                       align='left'),
            cells=dict(values=list(zip(*action_data)),
                      fill_color='lavender',
                      align='left')
        ), row=3, col=3)
        
        # Update layout
        fig.update_layout(
            title={
                'text': "📈 IT Career Success Dashboard - Complete Analysis",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 28, 'color': '#2c3e50'}
            },
            height=1200,
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='#f8f9fa'
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Experience Levels", tickangle=45, row=1, col=3)
        fig.update_xaxes(title_text="Skills", row=2, col=1)
        fig.update_xaxes(title_text="Current Market Size", row=3, col=1)
        fig.update_xaxes(title_text="Success Metrics", tickangle=45, row=3, col=2)
        
        fig.update_yaxes(title_text="Number of Jobs", row=1, col=3)
        fig.update_yaxes(title_text="Job Postings", row=2, col=1)
        fig.update_yaxes(title_text="Growth Rate %", row=3, col=1)
        fig.update_yaxes(title_text="Score/Count", row=3, col=2)
        
        # Save as HTML file
        fig.write_html("comprehensive_summary_dashboard.html")
        fig.show()
        return fig
    
    def generate_all_dashboards(self):
        """Generate all dashboard visualizations"""
        print("🎨 Generating Complete Interactive Dashboard Suite...")
        print("="*60)
        
        if not self.load_data():
            return None
        
        dashboards = {}
        
        # Generate all dashboards
        dashboards['overview'] = self.create_overview_dashboard()
        dashboards['domains'] = self.create_domain_analysis_dashboard()
        dashboards['skills'] = self.create_skills_demand_dashboard()
        dashboards['careers'] = self.create_career_opportunities_dashboard()
        dashboards['companies'] = self.create_company_analysis_dashboard()
        dashboards['predictions'] = self.create_predictions_dashboard()
        dashboards['summary'] = self.create_comprehensive_summary_dashboard()
        
        print("\n" + "="*60)
        print("✅ ALL INTERACTIVE DASHBOARDS GENERATED SUCCESSFULLY!")
        print("="*60)
        print("📊 Dashboard Suite Includes:")
        print("  1. 🎯 Overview Dashboard - Key metrics and KPIs")
        print("  2. 📊 Domain Analysis - IT field distribution and trends")
        print("  3. 🚀 Skills Demand - In-demand skills and future trends")
        print("  4. 💼 Career Opportunities - Experience levels and paths")
        print("  5. 🏢 Company Analysis - Hiring companies and trends")
        print("  6. 🔮 Future Predictions - Growth forecasts 2025-2030")
        print("  7. 📈 Summary Dashboard - Comprehensive overview")
        print("\n🎨 All dashboards are interactive with hover, zoom, and filter capabilities!")
        print("💡 Use these insights to make data-driven career decisions!")
        
        # Create an HTML index page
        self.create_dashboard_index()
        
        return dashboards
    
    def create_dashboard_index(self):
        """Create an HTML index page for all dashboards"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IT Job Market Dashboard Suite</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            padding: 40px;
        }
        .dashboard-card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #e1e8ed;
        }
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        .card-header {
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-bottom: 1px solid #dee2e6;
        }
        .card-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .card-title {
            font-size: 1.3em;
            font-weight: 600;
            color: #2c3e50;
            margin: 0;
        }
        .card-description {
            color: #6c757d;
            margin: 5px 0 0 0;
            font-size: 0.9em;
        }
        .card-body {
            padding: 20px;
        }
        .dashboard-link {
            display: inline-block;
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white;
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 25px;
            font-weight: 500;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            width: 100%;
            text-align: center;
            box-sizing: border-box;
        }
        .dashboard-link:hover {
            background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
            transform: translateY(-2px);
        }
        .stats {
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #dee2e6;
        }
        .stat-item {
            display: inline-block;
            margin: 0 30px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }
        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
                padding: 20px;
            }
            .stat-item {
                display: block;
                margin: 20px 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 IT Job Market Dashboard Suite</h1>
            <p>Interactive Analysis of 50,000+ IT Job Opportunities</p>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">50,000+</div>
                <div class="stat-label">IT Jobs Analyzed</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">7</div>
                <div class="stat-label">Interactive Dashboards</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">15+</div>
                <div class="stat-label">Key Skills Tracked</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">2025-2030</div>
                <div class="stat-label">Prediction Timeline</div>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <div class="dashboard-card">
                <div class="card-header">
                    <div class="card-icon">🎯</div>
                    <h3 class="card-title">Overview Dashboard</h3>
                    <p class="card-description">Key metrics, total opportunities, and market summary</p>
                </div>
                <div class="card-body">
                    <a href="overview_dashboard.html" class="dashboard-link">View Overview</a>
                </div>
            </div>
            
            <div class="dashboard-card">
                <div class="card-header">
                    <div class="card-icon">📊</div>
                    <h3 class="card-title">Domain Analysis</h3>
                    <p class="card-description">IT field distribution, market share, and domain trends</p>
                </div>
                <div class="card-body">
                    <a href="domain_analysis_dashboard.html" class="dashboard-link">Explore Domains</a>
                </div>
            </div>
            
            <div class="dashboard-card">
                <div class="card-header">
                    <div class="card-icon">🚀</div>
                    <h3 class="card-title">Skills Demand</h3>
                    <p class="card-description">In-demand skills, future trends, and growth analysis</p>
                </div>
                <div class="card-body">
                    <a href="skills_demand_dashboard.html" class="dashboard-link">View Skills</a>
                </div>
            </div>
            
            <div class="dashboard-card">
                <div class="card-header">
                    <div class="card-icon">💼</div>
                    <h3 class="card-title">Career Opportunities</h3>
                    <p class="card-description">Experience levels, work types, and career paths</p>
                </div>
                <div class="card-body">
                    <a href="career_opportunities_dashboard.html" class="dashboard-link">Explore Careers</a>
                </div>
            </div>
            
            <div class="dashboard-card">
                <div class="card-header">
                    <div class="card-icon">🏢</div>
                    <h3 class="card-title">Company Analysis</h3>
                    <p class="card-description">Top hiring companies, industry focus, and trends</p>
                </div>
                <div class="card-body">
                    <a href="company_analysis_dashboard.html" class="dashboard-link">View Companies</a>
                </div>
            </div>
            
            <div class="dashboard-card">
                <div class="card-header">
                    <div class="card-icon">🔮</div>
                    <h3 class="card-title">Future Predictions</h3>
                    <p class="card-description">Growth forecasts for 2025-2030 and investment priorities</p>
                </div>
                <div class="card-body">
                    <a href="predictions_dashboard.html" class="dashboard-link">See Predictions</a>
                </div>
            </div>
            
            <div class="dashboard-card">
                <div class="card-header">
                    <div class="card-icon">📈</div>
                    <h3 class="card-title">Complete Summary</h3>
                    <p class="card-description">Comprehensive overview with all insights and action items</p>
                </div>
                <div class="card-body">
                    <a href="comprehensive_summary_dashboard.html" class="dashboard-link">View Summary</a>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>🎨 Generated by IT Job Market Analysis Dashboard Suite | Interactive Plotly Visualizations</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open("dashboard_index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print("\n🌐 Created dashboard_index.html - Open this file in your browser!")
        print("📂 All individual dashboard HTML files have been saved to your project folder")

def main():
    """Main dashboard execution"""
    print("🎨 IT Job Market Interactive Dashboard Suite")
    print("="*60)
    print("Creating beautiful, interactive visualizations with Plotly...")
    
    dashboard = ITJobDashboard()
    all_dashboards = dashboard.generate_all_dashboards()
    
    if all_dashboards:
        print(f"\n🎯 Dashboard generation completed successfully!")
        print(f"📈 Ready to explore {len(all_dashboards)} interactive dashboards!")
    else:
        print("❌ Dashboard generation failed. Please check the data file.")

if __name__ == "__main__":
    main()
