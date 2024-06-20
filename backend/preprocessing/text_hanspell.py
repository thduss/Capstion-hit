from hanspell import spell_checker
import pandas as pd


def spell_check(text):
    result = spell_checker.check(text)
    return result.checked