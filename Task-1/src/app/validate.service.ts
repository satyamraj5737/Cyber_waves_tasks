import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ValidateService {

  constructor() { }
  validateData(data: any): boolean {
    // Implement validation logic
    return true; // Placeholder
  }
}
