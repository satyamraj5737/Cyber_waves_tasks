import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class StoreDataService {

  private storage: any[] = [];

  constructor() {}

  storeData(data: any): void {
    this.storage.push(data);
  }

  getData(): any[] {
    return this.storage;
  }
}
