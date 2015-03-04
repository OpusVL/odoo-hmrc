# odoo-hmrc


## `account_hmrc_esl_declaration`
WORK IN PROGRESS: ESL export for HMRC

Please note this module is under development, and does not yet work.

Current status is that the CSV headers can be got OK but there are no detail lines.

Also you need to provide your own logic to decide on whether a transaction is Triangular,
B2B Goods or B2B Services, or install `account_hmrc_constant_indicator`.

To provide your own logic, you must add `account_hmrc_esl_declaration` to an Odoo addon of your
own, do an `_inherit = 'account.move.line'` and implement the method `_transaction_indicator_type_compute`.

In the future, we may develop a default implementation that will calculate the correct transaction type
from other aspects of the move line.
However our current contract's requirement is to provide a constant one, which is implemented in
the `account_hmrc_constant_indicator` module detailed below.

## `account_hmrc_constant_indicator`

This provides an implementation of `_transaction_indicator_type_compute` which gets
the transaction indicator type from the account's company's 'Constant transaction indicator type'
field.

As a result of installing this, each company can have either 'B2B Goods', 'B2B Services' or
'Triangular' selected, and this will be the only type of line that is output.

You could also use this as an example of how to get started writing your own version of
`_transaction_indicator_type_compute`.
