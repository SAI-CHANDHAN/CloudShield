export type Severity = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO'
export type FindingStatus = 'OPEN' | 'RESOLVED' | 'SUPPRESSED'

export interface Resource {
  id: number
  resource_id: string
  resource_type: string
  provider: string
  region?: string | null
  name?: string | null
  created_at?: string | null
  updated_at?: string | null
}

export interface Finding {
  id: number
  finding_id: string
  resource_id: string
  resource_type: string
  title: string
  severity: Severity
  category: string
  rule_id: string
  status: FindingStatus
  risk_score: number
  created_at?: string | null
  updated_at?: string | null
}

export interface RiskSummary {
  overall_risk_score: number
  total_findings: number
  open_findings: number
  resolved_findings: number
  critical_count: number
  high_count: number
  medium_count: number
  low_count: number
  info_count: number
}

export interface ScanResponse {
  scan_status: string
  resources_scanned: number
  findings_created: number
  findings: Finding[]
}
