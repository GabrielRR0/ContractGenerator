import type { ContractData, FieldSpec } from '../../services/contractGenerator/contract.service'

export function validateRequiredFields(data: ContractData, campos: FieldSpec[], requiredSuffix: string): string[] {
  return campos.filter((campo) => !data[campo.name]?.trim()).map((campo) => `${campo.label} ${requiredSuffix}`)
}

export function validateFieldLengths(
  data: ContractData,
  campos: FieldSpec[],
  tooLongPrefix: string,
  tooLongSuffix: string,
): string[] {
  return campos
    .filter((campo) => campo.max_length != null && (data[campo.name]?.length ?? 0) > campo.max_length)
    .map((campo) => `${campo.label} ${tooLongPrefix}${campo.max_length!.toLocaleString()}${tooLongSuffix}`)
}
