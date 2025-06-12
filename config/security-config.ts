/*
 * Copyright (c) 2014-2025 Bjoern Kimminich & the OWASP Juice Shop contributors.
 * SPDX-License-Identifier: MIT
 */

import crypto from 'node:crypto'
import config from 'config'

export interface SecurityConfig {
  totpSecretEncryptionKey: string
}

// Retrieve the TOTP secret encryption key from environment variables or generate a secure one
const totpSecretEncryptionKey = process.env.TOTP_SECRET_ENCRYPTION_KEY || 
    (config.has('security.totpSecretEncryptionKey') ? 
    config.get('security.totpSecretEncryptionKey') : 
    crypto.randomBytes(32).toString('hex'))

// Export the security configuration
export const securityConfig: SecurityConfig = {
  totpSecretEncryptionKey
}

// Encryption helper for TOTP secrets
export const encryptTotpSecret = (plainText: string): string => {
  const iv = crypto.randomBytes(16)
  const key = Buffer.from(securityConfig.totpSecretEncryptionKey, 'hex').slice(0, 32)
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv)
  let encrypted = cipher.update(plainText, 'utf8', 'hex')
  encrypted += cipher.final('hex')
  return iv.toString('hex') + ':' + encrypted
}

// Decryption helper for TOTP secrets
export const decryptTotpSecret = (cipherText: string): string => {
  try {
    const parts = cipherText.split(':')
    if (parts.length !== 2) throw new Error('Invalid encrypted data format')
    
    const iv = Buffer.from(parts[0], 'hex')
    const encrypted = parts[1]
    const key = Buffer.from(securityConfig.totpSecretEncryptionKey, 'hex').slice(0, 32)
    const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv)
    let decrypted = decipher.update(encrypted, 'hex', 'utf8')
    decrypted += decipher.final('utf8')
    return decrypted
  } catch (error) {
    console.error('Failed to decrypt TOTP secret:', error)
    return '' // Return empty string on error
  }
}
