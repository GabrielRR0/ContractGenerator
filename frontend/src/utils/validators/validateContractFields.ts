import type { ContractData, FieldSpec } from '../../services/contractGenerator/contract.service'

export function validateRequiredFields(data: ContractData, campos: FieldSpec[], requiredSuffix: string): string[] {
  return campos.filter((campo) => !data[campo.name]?.trim()).map((campo) => `${campo.label} ${requiredSuffix}`)
}
