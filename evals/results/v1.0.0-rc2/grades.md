# Eval grades: v1.0.0-rc2

| Case | Run | Verdict | Recall | At severity | Missed | Should not flag | Judgment | Format | Invented numbers | Dashes |
|---|---|---|---|---|---|---|---|---|---|---|
| synthetic-backend-no-ai | skill | borderline ok | 4/4 | 4/4 | - | - | 0/0 | yes | - | 0 |
| synthetic-backend-no-ai | baseline | reject WRONG | 0/4 | 0/4 | ACH-1, ACH-6, SKL-4, SKL-10 | - | 0/0 | no | - | 0 |
| synthetic-devops-no-cloud | skill | reject ok | 3/3 | 3/3 | - | - | 1/1 | yes | - | 0 |
| synthetic-devops-no-cloud | baseline | reject ok | 0/3 | 0/3 | RED-2, REG-8, STR-12 | - | 0/1 | no | - | 0 |
| synthetic-region-flags | skill | borderline ok | 5/5 | 5/5 | - | - | 1/1 | yes | - | 0 |
| synthetic-region-flags | baseline | borderline ok | 0/5 | 0/5 | REG-7, REG-6, SKL-17, REG-2, REG-3 | - | 0/1 | no | - | 0 |
| synthetic-strong | skill | invite ok | 0/0 | 0/0 | - | - | 0/0 | yes | - | 0 |
| synthetic-strong | baseline | invite ok | 0/0 | 0/0 | - | - | 0/0 | no | - | 0 |

Recall of must_flag: skill 12/12, baseline 0/12.
Skill cases passing must_flag, must_not_flag and numbers: 4/4; verdicts right: 4/4.
Gate (spec 03 section 7): NOT met. The owner still reads the rewrites for quality.
