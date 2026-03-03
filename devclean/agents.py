"""
Multi-Agent Architecture for DevClean using OpenClaw
Agents handle specialized tasks in the disk cleanup workflow
"""

import os
import json
import subprocess
from collections import defaultdict
from typing import Dict, List, Any
import requests


class DiskAnalyzerAgent:
    """Agent responsible for disk analysis and file system scanning"""
    
    def __init__(self):
        self.name = "disk_analyzer"
        self.description = "Scans filesystem and analyzes disk usage by file type and folder"
    
    def analyze(self, root_path: str = ".") -> Dict[str, Any]:
        """Scan disk and categorize by file type and folder"""
        file_types = defaultdict(int)
        folder_sizes = defaultdict(int)
        
        for dirpath, dirnames, filenames in os.walk(root_path):
            for file in filenames:
                filepath = os.path.join(dirpath, file)
                try:
                    size = os.path.getsize(filepath)
                    ext = os.path.splitext(file)[1].lower()
                    
                    file_types[ext] += size
                    folder_sizes[dirpath] += size
                except:
                    continue
        
        return {
            "agent": self.name,
            "file_types": dict(file_types),
            "folders": dict(folder_sizes),
            "total_size": sum(file_types.values())
        }


class DockerAnalyzerAgent:
    """Agent responsible for Docker image and container analysis"""
    
    def __init__(self):
        self.name = "docker_analyzer"
        self.description = "Analyzes unused Docker images and dangling containers"
    
    def analyze(self) -> Dict[str, Any]:
        """Check for unused Docker images and volumes"""
        result = {
            "agent": self.name,
            "unused_images": [],
            "dangling_volumes": [],
            "stopped_containers": []
        }
        
        try:
            # Check for unused images
            images_output = subprocess.run(
                ["docker", "images", "--format", "{{.ID}} {{.Repository}} {{.Size}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if images_output.returncode == 0:
                result["unused_images"] = images_output.stdout.strip().split('\n')
            
            # Check for dangling volumes
            volumes_output = subprocess.run(
                ["docker", "volume", "ls", "--filter", "dangling=true"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if volumes_output.returncode == 0:
                result["dangling_volumes"] = volumes_output.stdout.strip().split('\n')
        
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            result["error"] = f"Docker analysis skipped: {str(e)}"
        
        return result


class PackageCacheAgent:
    """Agent responsible for identifying package manager caches"""
    
    def __init__(self):
        self.name = "cache_analyzer"
        self.description = "Identifies package manager caches (npm, pip, docker, etc.)"
    
    def analyze(self) -> Dict[str, Any]:
        """Scan for common package manager caches"""
        caches = {
            "agent": self.name,
            "npm_cache": None,
            "pip_cache": None,
            "docker_cache": None,
            "git_objects": None
        }
        
        home = os.path.expanduser("~")
        
        # npm cache
        npm_cache = os.path.join(home, ".npm")
        if os.path.exists(npm_cache):
            try:
                size = sum(os.path.getsize(os.path.join(dirpath, f)) 
                          for dirpath, _, filenames in os.walk(npm_cache) 
                          for f in filenames)
                caches["npm_cache"] = {"path": npm_cache, "size": size}
            except:
                pass
        
        # pip cache
        pip_cache = os.path.join(home, ".cache/pip")
        if os.path.exists(pip_cache):
            try:
                size = sum(os.path.getsize(os.path.join(dirpath, f)) 
                          for dirpath, _, filenames in os.walk(pip_cache) 
                          for f in filenames)
                caches["pip_cache"] = {"path": pip_cache, "size": size}
            except:
                pass
        
        # git objects
        git_cache = os.path.join(home, ".cache/git-rebase-merge")
        if os.path.exists(git_cache):
            try:
                size = sum(os.path.getsize(os.path.join(dirpath, f)) 
                          for dirpath, _, filenames in os.walk(git_cache) 
                          for f in filenames)
                caches["git_objects"] = {"path": git_cache, "size": size}
            except:
                pass
        
        return caches


class OptimizationAgent:
    """Agent responsible for generating AI-powered optimization recommendations"""
    
    def __init__(self, api_key: str = None):
        self.name = "optimization"
        self.description = "Generates AI-powered optimization recommendations"
        self.api_key = api_key
    
    def generate_recommendations(self, analysis_data: Dict[str, Any]) -> str:
        """Generate AI recommendations based on collected analysis"""
        
        if not self.api_key:
            return self._fallback_recommendations(analysis_data)
        
        # Format data for AI analysis
        analysis_summary = self._format_analysis(analysis_data)
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "DevClean - OpenClaw Multi-Agent Edition"
        }
        
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert DevOps engineer specializing in disk optimization and system performance.
                    
Analyze disk usage and provide specific, actionable recommendations for:
1. Files and folders to clean up (temp files, logs, caches)
2. Package manager caches to clear
3. Docker cleanup strategies
4. Development artifacts that can be removed
5. Compression and archival opportunities

Be specific about file paths, sizes, and the impact of each recommendation."""
                },
                {
                    "role": "user",
                    "content": f"""Based on this multi-agent analysis, provide optimization recommendations:

{analysis_summary}

Prioritize recommendations by potential space savings and safety."""
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"]
            else:
                return self._fallback_recommendations(analysis_data)
        
        except Exception as e:
            return f"AI analysis failed: {str(e)}. Using fallback recommendations.\n\n{self._fallback_recommendations(analysis_data)}"
    
    def _format_analysis(self, data: Dict[str, Any]) -> str:
        """Format collected agent data for AI analysis"""
        summary = "📊 **MULTI-AGENT ANALYSIS REPORT**\n\n"
        
        # Disk analysis
        if "disk" in data:
            disk = data["disk"]
            summary += "**Disk Analysis:**\n"
            file_types = disk.get("file_types", {})
            top_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:5]
            for ext, size in top_types:
                summary += f"  - {ext or 'No Ext'}: {self._format_bytes(size)}\n"
            summary += "\n"
        
        # Docker analysis
        if "docker" in data:
            docker = data["docker"]
            unused = docker.get("unused_images", [])
            if unused and unused[0]:
                summary += f"**Docker:** Found {len(unused)} images\n"
            summary += "\n"
        
        # Cache analysis
        if "caches" in data:
            caches = data["caches"]
            summary += "**Package Manager Caches:**\n"
            for cache_type, info in caches.items():
                if info and isinstance(info, dict) and "size" in info:
                    summary += f"  - {cache_type}: {self._format_bytes(info['size'])}\n"
            summary += "\n"
        
        return summary
    
    def _fallback_recommendations(self, data: Dict[str, Any]) -> str:
        """Provide recommendations without AI when API is unavailable"""
        return """🤖 **GenAI Recommendations** (Fallback Mode)

**Immediate Actions:**
1. Clear npm cache: `npm cache clean --force` (~100-500MB)
2. Clear pip cache: `pip cache purge` (~50-200MB)
3. Remove __pycache__ directories: `find . -type d -name __pycache__ -exec rm -rf {} +`
4. Clean Docker images: `docker image prune -a` (confirm first)

**Development Cleanup:**
- Remove node_modules from inactive projects
- Archive old Docker containers
- Clean up temporary build files

**Ongoing Maintenance:**
- Run cleanup weekly
- Monitor large log files
- Archive old project directories

*For detailed AI analysis, add OPENROUTER_API_KEY to .env*"""
    
    @staticmethod
    def _format_bytes(bytes_val: int) -> str:
        """Convert bytes to human-readable format"""
        if bytes_val == 0:
            return "0 Bytes"
        k = 1024
        sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
        i = min(len(sizes) - 1, int(__import__('math').log(bytes_val, k)))
        return f"{bytes_val / (k ** i):.2f} {sizes[i]}"


class OrchestratorAgent:
    """Master orchestrator agent that coordinates all specialized agents"""
    
    def __init__(self, api_key: str = None):
        self.name = "orchestrator"
        self.description = "Coordinates all cleanup agents in parallel and sequential workflows"
        self.disk_agent = DiskAnalyzerAgent()
        self.docker_agent = DockerAnalyzerAgent()
        self.cache_agent = PackageCacheAgent()
        self.optimization_agent = OptimizationAgent(api_key)
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """Run all agents in orchestrated workflow"""
        
        # Phase 1: Parallel data gathering
        analysis_result = {
            "workflow": "multi_agent_analysis",
            "agents": []
        }
        
        # Run disk analysis
        disk_analysis = self.disk_agent.analyze()
        analysis_result["agents"].append(disk_analysis)
        
        # Run docker analysis
        docker_analysis = self.docker_agent.analyze()
        analysis_result["agents"].append(docker_analysis)
        
        # Run cache analysis
        cache_analysis = self.cache_agent.analyze()
        analysis_result["agents"].append(cache_analysis)
        
        # Phase 2: Generate AI recommendations based on collected data
        combined_data = {
            "disk": disk_analysis,
            "docker": docker_analysis,
            "caches": cache_analysis
        }
        
        recommendations = self.optimization_agent.generate_recommendations(combined_data)
        analysis_result["recommendations"] = recommendations
        
        return analysis_result
