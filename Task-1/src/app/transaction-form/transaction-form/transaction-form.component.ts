import { Component } from '@angular/core';
import { AnonymizeService } from '../../anonymize.service';
import { EncryptService } from '../../encrypt.service';
import { RiskAssessmentService } from '../../risk-assessment.service';
import { StoreDataService } from '../../store-data.service';
import { ValidateService } from '../../validate.service';

@Component({
  selector: 'app-transaction-form',
  templateUrl: './transaction-form.component.html',
  styleUrls: ['./transaction-form.component.scss']
})
export class TransactionFormComponent {
  transaction = {
    transactionId: '',
    userId: '',
    transactionDetails: {
      amount: 0,
      currency: '',
      transactionDate: '',
      paymentMethod: '',
      merchantDetails: {
        merchantId: '',
        name: '',
        category: '',
        countryCode: ''
      }
    },
    userDetails: {
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      billingAddress: {
        street: '',
        city: '',
        state: '',
        postalCode: '',
        country: ''
      }
    },
    additionalInfo: {
      deviceIp: '',
      userAgent: ''
    }
  };

  constructor(
    private anonymizeService: AnonymizeService,
    private encryptService: EncryptService,
    private riskAssessmentService: RiskAssessmentService,
    private storeDataService: StoreDataService,
    private validateService: ValidateService
  ) {}

  onSubmit() {
    if (this.validateService.validateData(this.transaction)) {
      const anonymizedData = this.anonymizeService.anonymizeData(this.transaction);
      const encryptedData = this.encryptService.encryptData(anonymizedData);
      const riskScore = this.riskAssessmentService.assessRisk(encryptedData);
      this.storeDataService.storeData({ encryptedData, riskScore });
    } else {
      alert('Invalid data');
    }
  }
}
