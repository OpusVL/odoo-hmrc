# odoo-hmrc

Tools to assist you with data submissions to Her Majesty's Revenue and Customs.

Currently this module contains the ESL declaration and a sample module for
deciding the Indicator Code to use on those declarations.

## `account_hmrc_esl_declaration`
WORK IN PROGRESS: ESL export for HMRC

Please note this module is under development, and does not yet work.

When it does, it will provide you with a tool to export a CSV file in the correct
format for electronically submitting your ESL declaration (VAT101) to HMRC online.

Current status is that the CSV headers can be got OK but there are no detail lines.

Also you need to provide your own logic to decide on whether a transaction is Triangular,
B2B Goods or B2B Services, or install `account_hmrc_constant_indicator`.

To provide your own logic, you must add `account_hmrc_esl_declaration` to the dependencies of an Odoo addon of your
own, do an `_inherit = 'account.move.line'` and implement the method `_transaction_indicator_type_compute`.

In the future, we may develop a default implementation that will calculate the correct transaction type
from other aspects of the move line.
However our current contract's requirement is to provide a constant one, which is implemented in
the `account_hmrc_constant_indicator` module detailed below.

### Current status and limitations

* Currently this only outputs the two header lines.  The algorithm for calculating the detail lines remains to be written.
* Currently, there is only one implementation of the logic to choose the Indicator Code, and that is in `account_hmrc_constant_indicator`.  The default implementation is abstract, so you need to install the aforementioned constant indicator module or write your own.  If another implementation is found that reliably makes the right choice for any installation, we may make that implementation the default.

## `account_hmrc_constant_indicator`

This provides an implementation of `_transaction_indicator_type_compute` which gets
the transaction indicator type from the account's company's 'Constant transaction indicator type'
field.

As a result of installing this, each company can have either 'B2B Goods', 'B2B Services' or
'Triangular' selected, and this will be the only type of line that is output.

You can find this setting in Settings -> Companies -> `Your Company` -> Configuration

You could also use this as an example of how to get started writing your own version of
`_transaction_indicator_type_compute`.


## Current overall limitations

Apart from limitations given under individual addons' sections above:

* The API and addon structure is in flux.  We may refactor these in such a way that, for example, if you implement your own `_transaction_indicator_type_compute`, and import the `INDICATOR_SELECTION` list, you may have to change the import in the future.


# Copyright and License

Copyright (C) 2015 OpusVL

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

If you require assistance, support, or further development of this
software, please contact OpusVL using the details below:

* Telephone: +44 (0)1788 298 410
* Email: community@opusvl.com
* Web: http://opusvl.com

