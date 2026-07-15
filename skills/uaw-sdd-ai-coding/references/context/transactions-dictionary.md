# Transaction 字典历史快照

## 来源与使用边界

- 运行时职责：上下文快照，不是当前系统字典的权威来源。
- 迁移来源：`original/project-how-to/detailed-context/2.transactions字典清单.md`。
- 来源内容与运行时内容一致性确认日期：`2026-07-14`。
- 添加本来源说明前的源文件 SHA-256：`e9afbb3222a3ca6327949810a745e3132b18ce3d236426d2bb28ef94097bb372`。
- 首次导入运行时的 Commit：`03855a81255c4b8a5037758d7cba783bd56596fe`。
- 业务所有者/当前权威系统：未记录；每次使用都必须重新确认。

下列名称、候选包、Sprint/就绪标签、依赖和下拉值都是历史候选数据。在 Spec、Design、代码、数据库脚本或测试中使用前，必须用当前代码、配置、Schema、API 或当前用户确认进行核对，并记录确认来源和时间。缺失值继续视为未知，不得推断。

## 提取内容

本快照包含候选 Transaction Type 和相关字段选项。表格内英文属于历史业务数据原值，不代表当前语言规范，也不得在未确认时直接转为需求。

该表格涵盖了从“Enquiry & Information”到“Change Status”等不同模块下的所有交易类型，并补充了文件中涉及的下拉选项（如 Title、Cancel Reason 等）。

### 1. Transaction Type 字典表 (业务交易类型)

| 模块 | 交易类型 | Java驼峰命名 | Package命名 | Sprint / 状态 | 备注/依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Enquiry & Information** | **Payment Information** | paymentInformation | com.ocft.iic.uaw.server.modules.cases.paymentinformation | Ready (Sprint4) | N |
| **Enquiry & Information** | **Policy Information** | policyInformation | com.ocft.iic.uaw.server.modules.cases.policyinformation | Ready (Sprint4) | N |
| **Enquiry & Information** | **Policy Values** | policyValues | com.ocft.iic.uaw.server.modules.cases.policyvalues | Ready (Sprint4) | N |
| **Enquiry & Information** | **Premium Information** | premiumInformation | com.ocft.iic.uaw.server.modules.cases.premiuminformation | Ready (Sprint4) | N |
| **Enquiry & Information** | **Death Claim Enquiry** | deathClaimEnquiry | com.ocft.iic.uaw.server.modules.cases.deathclaimenquiry | Ready (Sprint4) | Current UAW doesn't include the Claim Query |
| **Enquiry & Information** | **Errors and Issues** | errorsAndIssues | com.ocft.iic.uaw.server.modules.cases.errorsandissues | Ready (Sprint4) | N |
| **Enquiry & Information** | **OM Enquiry** | omEnquiry | com.ocft.iic.uaw.server.modules.cases.omenquiry | Ready (Sprint4) | N |
| **Enquiry & Information** | **Overpayment Recovery/Missed Premiums** | overpaymentRecoveryMissedPremiums | com.ocft.iic.uaw.server.modules.cases.overpaymentrecoverymissedpremiums | Ready | Y (M65 Report dependency) |
| **Enquiry & Information** | **SASSA General Enquiry** | sassaGeneralEnquiry | com.ocft.iic.uaw.server.modules.cases.sassageneralenquiry | No resource | |
| **Enquiry & Information** | **SASSA Claim Enquiry** | sassaClaimEnquiry | com.ocft.iic.uaw.server.modules.cases.sassaclaimenquiry | No resource | |
| **Enquiry & Information** | **Document Requested** | documentRequested | com.ocft.iic.uaw.server.modules.cases.documentrequested | 90% Ready | Y (Ref Library/Related case dependency) |
| **Enquiry & Information** | **Specific Service Request** | specificServiceRequest | com.ocft.iic.uaw.server.modules.cases.specificservicerequest | 90% Ready | N |
| **Enquiry & Information** | **Follow Up on Previous Requests** | followUpOnPreviousRequests | com.ocft.iic.uaw.server.modules.cases.followuponpreviousrequests | Ready | Y (Details/comments saving pot related) |
| **Enquiry & Information** | **Submit Documents Only** | submitDocumentsOnly | com.ocft.iic.uaw.server.modules.cases.submitdocumentsonly | No resource | |
| **Change Status** | **Change My Beneficiary Details** | changeMyBeneficiaryDetails | com.ocft.iic.uaw.server.modules.cases.changemybeneficiarydetails | √ | Y (Validation Required, banking?) |
| **Change Status** | **Change My cashback recipient details** | changeMyCashbackRecipientDetails | com.ocft.iic.uaw.server.modules.cases.changemycashbackrecipientdetails | | Y |
| **Change Status** | **Change My Correspondent Detail** | changeMyCorrespondentDetail | com.ocft.iic.uaw.server.modules.cases.changemycorrespondentdetail | | |
| **Change Status** | **Change Dependant/Life Assured Details** | changeDependantLifeAssuredDetails | com.ocft.iic.uaw.server.modules.cases.changedependantlifeassureddetails | | |
| **Change Status** | **Change Life Assured Details** | changeLifeAssuredDetails | com.ocft.iic.uaw.server.modules.cases.changelifeassureddetails | | |
| **Change Status** | **Change My premium Payer Details** | changeMyPremiumPayerDetails | com.ocft.iic.uaw.server.modules.cases.changemypremiumpayerdetails | | |
| **Change Status** | **Change My Replacement Policy Owner Details** | changeMyReplacementPolicyOwnerDetails | com.ocft.iic.uaw.server.modules.cases.changemyreplacementpolicyownerdetails | | Y (Validation Required, banking?) |
| **Change Status** | **Change My Security Cession Details** | changeMySecurityCessionDetails | com.ocft.iic.uaw.server.modules.cases.changemysecuritycessiondetails | | N |
| **Change Status** | **Change My Policy Owner** | changeMyPolicyOwner | com.ocft.iic.uaw.server.modules.cases.changemypolicyowner | | |
| **Change Status** | **Switch My Investment Funds** | switchMyInvestmentFunds | com.ocft.iic.uaw.server.modules.cases.switchmyinvestmentfunds | √ | N (Free text Input, no validation) |
| **Change Status** | **Change Date of Birth** | changeDateOfBirth | com.ocft.iic.uaw.server.modules.cases.changedateofbirth | Sprint4 | |
| **Change Status** | **Change of Contact Details** | changeOfContactDetails | com.ocft.iic.uaw.server.modules.cases.changeofcontactdetails | Sprint4 | Y (GCS Validation) |
| **Change Status** | **Change of Tax Details** | changeOfTaxDetails | com.ocft.iic.uaw.server.modules.cases.changeoftaxdetails | Sprint4 | |
| **Change Status** | **Change Personal Details** | changePersonalDetails | com.ocft.iic.uaw.server.modules.cases.changepersonaldetails | Sprint4 | |
| **Change Status** | **Change My Intermediary** | changeMyIntermediary | com.ocft.iic.uaw.server.modules.cases.changemyintermediary | | N (Advisor Appointment Form) |

---

### 2. 相关通用字段字典表

以下是文件中提到的各类下拉框及选项的详细字典数据。

#### A. Service Group (服务组)
- Money
- Change Status
- Enquiry & Information

#### B. Brand (品牌/产品系列)
- Greenlight
- Flexi
- Conventional
- Annuity
- Essentials
- Investment Frontiers
- Unit Trusts
- Professional Income Protection Plan
- Nedbank
- Compass
- Fairbairn Capital
- Investment Horizons
- Old Mutual Max Income
- Old Mutual Max Investments
- Old Mutual Max Investments Namibia
- Greenlight Namibia
- Greenlight Offshore
- Investment Horizons Guernsey
- Investment Horizons Namibia
- Group Schemes Voluntary Group
- Group Schemes Growplan
- Defined Contribution Umbrella
- Group Assurance Products
- Investment Solutions
- Mosaic
- Old Mutual Superfund
- Orion
- Unclaimed Benefit Fund
- Old Mutual Invest
- Old Mutual Wealth
- Old Mutual Protect
- Old Mutual Savings
- OM Unit Trusts
- SIS Unit Trusts
- Old Mutual Income
- Protektor Preservation Pension Fund
- Protektor Preservation Provident Fund
- Old Mutual SuperFund Provident Fund
- Independent Schools Association of Southern Africa Retirement Fund
- Independent Schools Association of Southern Africa Provident Fund
- Saccawu National Provident Fund
- Sacwu National Provident Fund

#### C. Title (称谓/头衔)
- ME
- MEJ
- MEV
- MISS
- MNR
- MRS
- MS
- MX
- BISHOP
- BISKOP
- PASTOOR
- PASTOR
- PROF
- REV
- RABBI
- RABBYN
- DR
- DR PROF
- DS

#### D. Service Result (服务结果)
- Proceed (Default)
- Cancel

#### E. Approve Reason (批准原因)
- Transaction complete - no further processing
- Submit for additional processing

#### F. Cancel Reason (取消原因)
- Customer decided not to continue with transaction
- Customer has decided not to continue with engagement
- Customer left before resuming transaction
- Duplicate claim request
- Insufficient documents to continue with transaction
- Selected incorrect service catalogue
- System is unavailable

#### G. ID Type (证件类型)
*(注：文件中提及为Dropdown但未列出具体值，需确认)*

#### H. Relationship Type (关系类型)
*(注：文件中提及为Dropdown但未列出具体值，需确认)*

#### I. Address Type (地址类型)
*(注：文件中提及为Dropdown但未列出具体值，需确认)*

#### J. Email Type (邮箱类型)
*(注：文件中提及为Dropdown但未列出具体值，需确认)*

#### K. Phone Type (电话类型)
*(注：文件中提及为Dropdown但未列出具体值，需确认)*

#### L. Account Type (账户类型)
*(注：银行账户类型，文件中提及为Dropdown但未列出具体值)*
