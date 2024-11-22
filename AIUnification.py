def unify(expr1, expr2):
    """
    Unify two expressions expr1 and expr2.
    Handles predicates and arguments as well as variables/constants.
    """
    # Case 1: If expr1 and expr2 are identical, return NIL (no substitution needed).
    if expr1 == expr2:
        return {}

    # Case 2: If expr1 is a variable, unify it with expr2.
    if is_variable(expr1):
        if occurs_check(expr1, expr2):
            return "FAILURE"  # Prevent circular substitution
        return {expr1: expr2}

    # Case 3: If expr2 is a variable, unify it with expr1.
    if is_variable(expr2):
        if occurs_check(expr2, expr1):
            return "FAILURE"  # Prevent circular substitution
        return {expr2: expr1}

    # Case 4: If both are compound terms (e.g., predicates with arguments).
    if is_compound(expr1) and is_compound(expr2):
        # Check if predicates are the same
        if get_predicate(expr1) != get_predicate(expr2):
            return "FAILURE"

        # Unify arguments
        args1 = get_arguments(expr1)
        args2 = get_arguments(expr2)

        if len(args1) != len(args2):
            return "FAILURE"  # Number of arguments must match

        # Process each argument recursively
        substitution = {}
        for arg1, arg2 in zip(args1, args2):
            # Apply current substitutions to arguments before unifying
            arg1 = apply_substitution(arg1, substitution)
            arg2 = apply_substitution(arg2, substitution)
            result = unify(arg1, arg2)
            if result == "FAILURE":
                return "FAILURE"
            substitution = combine_substitutions(substitution, result)

        return substitution

    # Case 5: If both are constants but not identical, return FAILURE.
    return "FAILURE"


def combine_substitutions(sub1, sub2):
    """
    Combine two substitutions into one.
    Apply sub2 to sub1 and merge them.
    """
    for var in sub1:
        sub1[var] = apply_substitution(sub1[var], sub2)
    sub1.update(sub2)
    return sub1


def is_variable(x):
    """Check if x is a variable (string starting with a lowercase letter)."""
    return isinstance(x, str) and x.islower()


def is_compound(expr):
    """Check if expr is a compound term (list or tuple with a predicate and arguments)."""
    return isinstance(expr, (list, tuple)) and len(expr) > 0


def get_predicate(expr):
    """Extract the predicate from a compound expression."""
    return expr[0] if is_compound(expr) else None


def get_arguments(expr):
    """Extract the arguments from a compound expression."""
    return expr[1:] if is_compound(expr) else []


def occurs_check(var, expr):
    """Check if the variable `var` occurs in the expression `expr`."""
    if var == expr:
        return True
    if is_compound(expr):
        return any(occurs_check(var, sub) for sub in get_arguments(expr))
    return False


def apply_substitution(expr, substitution):
    """Apply a substitution to an expression."""
    if is_variable(expr):
        while expr in substitution:
            expr = substitution[expr]
        return expr
    if is_compound(expr):
        return [apply_substitution(arg, substitution) for arg in expr]
    return expr


# Testing the updated unify function

# Example 1: Unifying variables and constants
expr1 = ["Eats", "x", "Apple"]
expr2 = ["Eats", "Riya", "y"]
result1 = unify(expr1, expr2)
print("Example 1:", result1)  # Output: {'x': 'Riya', 'y': 'Apple'}

# Example 2: Different predicates (should fail)
expr1 = ["Eats", "x", "Apple"]
expr2 = ["Drinks", "Riya", "y"]
result2 = unify(expr1, expr2)
print("Example 2:", result2)  # Output: FAILURE

# Example 3: Circular substitution (should fail)
expr1 = ["Eats", "x", "y"]
expr2 = ["Eats", ["f", "x"], "Apple"]  # Representing f(x) as ["f", "x"]
result3 = unify(expr1, expr2)
print("Example 3:", result3)  # Output: FAILURE

# Example 4: Nested structures with variables
expr1 = ["Knows", ["Father", "x"], "y"]
expr2 = ["Knows", ["Father", "John"], "z"]
result4 = unify(expr1, expr2)
print("Example 4:", result4)  # Output: {'x': 'John', 'y': 'z'}

# Example 5: Identical expressions (no substitution needed)
expr1 = ["Loves", "Apple", "Orange"]
expr2 = ["Loves", "Apple", "Orange"]
result5 = unify(expr1, expr2)
print("Example 5:", result5)  # Output: {}
