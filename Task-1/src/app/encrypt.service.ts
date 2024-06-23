import { Injectable } from '@angular/core';
import * as crypto from 'crypto';

@Injectable({
  providedIn: 'root'
})
export class EncryptService {

  private aesKey: Buffer = crypto.randomBytes(32);
  private iv: Buffer = crypto.randomBytes(16);

  constructor() {}

  encryptData(data: any): string {
    const cipher = crypto.createCipheriv('aes-256-cbc', this.aesKey, this.iv);
    let encrypted = cipher.update(JSON.stringify(data), 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return encrypted;
  }

  decryptData(encryptedData: string): any {
    const decipher = crypto.createDecipheriv('aes-256-cbc', this.aesKey, this.iv);
    let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return JSON.parse(decrypted);
  }
}
