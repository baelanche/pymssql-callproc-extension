# pymssql-callproc-extension
https://github.com/pymssql/pymssql extension module (callproc function)

## Installation

`pip install -r ./requirements.txt`

## Practice

### 1. create table

```sql
use test

create table books (
	idx int,
	title varchar(100)
)

insert into dbo.books values(1, 'a')
insert into dbo.books values(2, 'b')
insert into dbo.books values(3, 'c')
insert into dbo.books values(4, 'd')
insert into dbo.books values(5, 'e')
insert into dbo.books values(6, 'f')
insert into dbo.books values(7, 'g')
insert into dbo.books values(8, 'h')
insert into dbo.books values(9, 'i')
insert into dbo.books values(10, 'j')
```

### 2. create procedure and write codes (no outputs)

```sql
use test
go

create procedure dbo.get_book (
	@idx int
)
as
begin
	set nocount on

	select idx, title
	from dbo.books
	where idx = @idx

	set nocount off
end
```

```python
from pymssql_extension import Mssql

def get_mssql_session():
    mssql = Mssql()
    try:
        yield mssql
    finally:
        mssql.session.close()

db_generator = get_mssql_session()

db = next(db_generator)

result = db.stored_procedure('dbo.get_book', {'idx': 5})

print(result)
```

output:
```sh
[(5, 'e')]
```

### 3. create procedure and write codes (outputs)

```sql
use test
go

create procedure dbo.get_book_with_outputs (
	@idx int,
	@total int output,
	@position int output
)
as
begin
	set nocount on

	select idx, title
	from dbo.books
	where idx = @idx

	select @total = count(*)
	from dbo.books

	set @position = @total / 10

	set nocount off
end
```

```python
from pymssql_extension import Mssql

def get_mssql_session():
    mssql = Mssql()
    try:
        yield mssql
    finally:
        mssql.session.close()

db_generator = get_mssql_session()

db = next(db_generator)

result, outputs = db.stored_procedure('dbo.get_book_with_outputs', {'idx': 5}, {'total': 0, 'position': 0})

print(result)
print(outputs)
```

output:
```sh
[(5, 'e')]
[(10, 1)]
```
