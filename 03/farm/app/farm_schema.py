from schema import (
    And,
    Const,
    Forbidden,
    Hook,
    Literal,
    Optional,
    Or,
    Regex,
    Schema,
    SchemaError,
    SchemaForbiddenKeyError,
    SchemaMissingKeyError,
    SchemaUnexpectedTypeError,
    SchemaWrongKeyError,
    Use,
)

# enum for species
SpeciesSchema = Schema(["chicken", "cow"])

# enum for sex
SexSchema = Schema(["female", "male"])

DateSchema = Regex(r'[0-9]{4}\-[0-9]{4}\-[0-9]{2}')

AnimalSchema = Schema({
    "id": str,
    "species" : SpeciesSchema,
    "sex": SexSchema,
    Optional("dob"): DateSchema,
    # weight in grams? Or rather have it in a time-series db?
    Optional("weight"): And(Use(int), lambda w: 0 < w <= 10000000),
})
