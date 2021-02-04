from pydantic import BaseModel
from typing import Dict, List


class Cluster(BaseModel):
    name: str
    url: str
    token: str
    id: str


class Helm(BaseModel):
    parameters: Dict[str, str] = None


class RancherSource(BaseModel):
    filters: Dict[str, str] = None
    labels: Dict[str, str] = None
    ignore: List[str] = None


class GkeSource(BaseModel):
    filters: Dict[str, str] = None
    tags: Dict[str, str] = None
    ignore: List[str] = None


class EnforcementSource(BaseModel):
    rancher: RancherSource = None
    gke: GkeSource = None


class Enforcement(BaseModel):
    name: str
    repo: str
    path: str = None
    namespace: str = "default"
    helm: Helm = None


class ClusterRule(BaseModel):
    enforcements: List[Enforcement]
    source: EnforcementSource


class ClusterRuleStatus(BaseModel):
    clusters: List[dict]