# Library imports 
import pandas as pd 
import scipy.stats as stats
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multicomp import MultiComparison
import itertools


def decision(p_value:float, sig_level:float) -> str:
    """
    Make a decision based on the p-value and significance level.
    NB ..No df with nan values allowed

    Parameters:
    p_value (float): The p-value from the statistical test.
    sig_level (float): The significance level for the test.

    Returns:
    str: Decision statement based on the comparison of p-value and significance level.
    """
    if p_value >= sig_level:
        print(f"Fail to Reject the Null Hypothesis in favour of the alternative hypothesis because p-value:{p_value:.5f} is greater/equal to the significance level {sig_level}")
    else:
        print(f"Accept the Alternative Hypothesis:because p-value:{p_value:.5f} is less than the significance level {sig_level}\n")


################## START OF TESTS FOR NORMALITY #####################################

def Shapiro__Test(df:pd.DataFrame, df_column:str, Sig_level:float=0.05):
    """
    used to test for normality in the dataset for data where n < 2_000
    Null hypothesis:the data is normally distributed. 
        
    Parameters:

    df (pd.DataFrame): The DataFrame containing the data.
    df_column (str): The column name from DataFrame df to be tested.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level

    """
    
    shapiro_stat , P_value = stats.shapiro(df[df_column][:2_000]) # Subset for performance
    print(f"Shapiro-Wilk Test: {df_column}")
    print("======================================================================================================")
    print(f"Shapiro-Wilk Test: {shapiro_stat}, p-value: {P_value}\n")
    return decision(p_value=P_value, sig_level=Sig_level)



def Kolmogorov_Smirnov_Test(df:pd.DataFrame, df_column:str,type:str="norm", Sig_level:float=0.05):
    """
    used to test for normality in the dataset for data where n >= 2_000
    Null hypothesis:the data is normally distributed. 
        
    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    df_column (str): The column name from DataFrame df to be tested.
    type(str): The type of distribution your testing against
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level

    """
    ks_stat , P_value = stats.kstest(df[df_column], type)
    print(f"Kolmogorov-Smirnov Test: {df_column}")
    print("======================================================================================================")
    print(f"Kolmogorov-Smirnov Test: {ks_stat}, p-value: {P_value}\n")
    return decision(p_value=P_value, sig_level=Sig_level)

################## END OF TESTS FOR NORMALITY #####################################


################## START OF ONE GROUP STATISTICAL TESTS #####################################
def Cat_chisquare_1sam(df:pd.DataFrame, df_column:str, expected_obs, Sig_level:float=0.05):
    """
    Perform a chi-squared goodness-of-fit test on a categorical column.
    Used when you have a one sample categorical/Nominal variable eg YES or NO and an expected observations.
    NB ..No df with nan values allowed.
    Null hypothesis : No difference
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    df_column (str): The column name from DataFrame df to be tested.
    expected_obs (list): The expected frequencies for the categories.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    """
    
    chi2_stat , P_value = stats.chisquare(f_obs=df[df_column], f_exp=expected_obs)
    print(f"Chi-squared test for {df_column}:")
    print("======================================================================================================")
    print(f"Chi2 Stat: {chi2_stat}, p-value: {P_value}\n")
    return decision(p_value=P_value, sig_level=Sig_level)
    
def Ordinal_Wilicoxon_1sam(df:pd.DataFrame, df_column:str, alternative_side:str="two_sided", Sig_level:float=0.05):
    """
    Perform a Wilcoxon signed-rank test on an ordinal column.
    used on unknown distribution or non normally distributed ordinal/interval/ratio data only.
    NB..No df with nan values allowed.
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    df_column (str): The column name from DataFrame df to be tested.
    alternative_side (str, optional): The alternative hypothesis ('two-sided', 'greater', or 'less'). Default is 'two-sided'.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    """
    w_stat , P_value = stats.wilcoxon(df[df_column], alternative=alternative_side)
    print(f"Wilcoxon signed-rank test for  {df_column}:")
    print("======================================================================================================")
    print(f"W Stat: {w_stat}, p-value: {P_value}\n")
    return decision(p_value=P_value, sig_level=Sig_level)

def Ttest_1sam(df:pd.DataFrame, df_column:str, POP_mean, alternative_side:str='two-sided', Sig_level:float=0.05):
    """
    Perform a one-sample t-test on a numerical column.
    used on normally distributed interval/ratio data only
    NB ..No df with nan values allowed
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    df_column (str): The column name from DataFrame df to be tested.
    POP_mean (float): The population mean to compare against.
    alternative_side (str, optional): The alternative hypothesis ('two-sided', 'greater', or 'less'). Default is 'two-sided'.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    """
    
    t_stat , P_value = stats.ttest_1samp(df[df_column], popmean=POP_mean, alternative=alternative_side)
    print(f"One-sample t-test for {df_column}:")
    print("======================================================================================================")
    print(f"T Stat: {t_stat}, p-value: {P_value}\n")
    return decision(p_value=P_value, sig_level=Sig_level)
    
################## END OF ONE GROUP STATISTICAL TESTS #####################################


################## START OF TWO GROUP STATISTICAL TESTS ####################################################################
#####  start of two groups (independant samples) ########
def Man_whiteny_2sam_diff(df:pd.DataFrame, group1:str, group2:str, alternative_side:str='two-sided', Sig_level:float=0.05):
    """
    Perform the Mann-Whitney U test on two independent samples.
    used on unknown distribution or non normally distributed ordinal/interval/ratio data only.
    NB.. No df with nan values allowed.
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    group1_column (str): The column name for the first group.
    group2_column (str): The column name for the second group.
    alternative_side (str, optional): The alternative hypothesis ('two-sided', 'greater', or 'less'). Default is 'two-sided'.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    """
    u_stat, P_value = stats.mannwhitneyu(df[group1], df[group2], alternative=alternative_side)
    print(f"Mann-Whitney U test for {group1} & {group2}:")
    print("======================================================================================================")
    print(f"U Stat: {u_stat}, p-value: {P_value}\n")
    return decision(p_value=P_value, sig_level=Sig_level)

def Ttest_2sam(df:pd.DataFrame, group1:str, group2:str, alternative_side:str='two-sided', Sig_level:float=0.05):
    """
    Perform a two-sample t-test on two independent samples.
    used on normally distributed  interval/ratio data only.
    NB..No df with nan values allowed
    Null hypothesis : No difference
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    group1_column (str): The column name for the first group.
    group2_column (str): The column name for the second group.
    alternative_side (str, optional): The alternative hypothesis ('two-sided', 'greater', or 'less'). Default is 'two-sided'.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    """

    t_stat , P_value = stats.ttest_ind(df[group1], df[group2], alternative=alternative_side)
    print(f"Two-sample t-testfor {group1} & {group2}:")
    print("======================================================================================================")
    print(f"T Stat: {t_stat}, p-value: {P_value}\n")
    return decision(p_value=P_value, sig_level=Sig_level)

#fisher needs further implementation
def Fisher_2sam(df:pd.DataFrame, group_column1:str, group_column2:str, Sig_level:float=0.05):
    """
    Perform Fisher's exact test on a 2x2 contingency table.
    used on unknown distribution or non normally distributed categorical data only.
    Null hypothesis : No difference

    Parameters:
    df (list): A 2x2 contingency table.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    
    """
    table = pd.crosstab(df[group_column1], df[group_column2])
    oddsratio , P_value = stats.fisher_exact(table)
    print(f"Fisher's exact test {table.columns}:")
    print("======================================================================================================")
    print(f"Odds Ratio: {oddsratio}, p-value: {P_value}\n")
    return decision(p_value=P_value, sig_level=Sig_level)
#####  end of two groups (independant samples) ########

#####  start of  dependant two group samples (same people) ########
def Wilcoxon_Ranksum_2sam_dep(df: pd.DataFrame, before_column: str, after_column: str, alternative_side:str='two-sided', Sig_level: float = 0.05) -> str:
    """
    Perform a Wilcoxon signed-rank test on two dependent samples.
    Used when the data has an unknown distribution or non normal distribution use case on (ordinal and interval/ratio data)
    no nan data in df allowed
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    before_column (str): The column name for the before measurements.
    after_column (str): The column name for the after measurements.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    """
    w_stat, P_value = stats.wilcoxon(df[before_column], df[after_column], alternative=alternative_side)
    print(f"Wilcoxon signed-rank test for {before_column} and {after_column}:")
    print("======================================================================================================")
    print(f"W Stat: {w_stat}, p-value: {P_value}\n")
    return decision(p_value=P_value, sig_level=Sig_level)
    
def Paired_ttest_2sam(df:pd.DataFrame, before_column:str, after_column:str, alternative_side:str='two-sided', Sig_level:float = 0.05) -> str:
    """
        Perform a paired t-test on two dependent samples.
        Used when the data is normally distributed data use case on(ratio/interval data)
        non nan data allowed in df
        Null hypothesis : No difference

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        before_column (str): The column name for the before measurements.
        after_column (str): The column name for the after measurements.
        Sig_level (float, optional): The significance level for the test. Default is 0.05.

        Returns:
        str: Result of the decision function based on the p-value and significance level.
        """
    t_stat, P_value = stats.ttest_rel(df[before_column], df[after_column], alternative=alternative_side)
    print(f"Paired t-test for {before_column} and {after_column}:")
    print("======================================================================================================")
    print(f"T Stat: {t_stat}, p-value: {P_value}\n")
    return decision(p_value=P_value, sig_level=Sig_level)
    
def Mcnemar_test_2sam(df: pd.DataFrame, group1_column: str, group2_column: str,  Sig_level: float = 0.05) -> str:

    """
    Perform McNemar's test on paired nominal data.
    no nans allowed in df 
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    group1_column (str): The column name for the first group.
    group2_column (str): The column name for the second group.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    """
    table = pd.crosstab(df[group1_column], df[group2_column])
    result = mcnemar(table, exact=True)
    print(f"McNemar's test for {group1_column} and {group2_column}:")
    print("======================================================================================================")
    print(f"Statistic: {result.statistic}, p-value: {result.pvalue}\n")
    return decision(p_value=result.pvalue, sig_level=Sig_level)
################## end of dependant two group samples (same people)  #####################################

################## END OF TWO GROUP STATISTICAL TESTS #####################################

##########  START OF THREE GROUP OR MORE  STATISTICAL TESTS #################################
################## Start of tests for independent groups #####################################

def kruskal_wallis_test(df: pd.DataFrame, column: str, group_column: str, Sig_level: float = 0.05) -> str:
    """
    Perform the Kruskal-Wallis H test on three or more independent groups.
    used when data is not normally distributed and is ordinal or interval/ratio
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    column (str): The column name of the variable.
    group_column (str): The column name of the groups.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    """
    groups = [group[column].values for name, group in df.groupby(group_column)]
    stat, p_value = stats.kruskal(*groups)
    print(f"Kruskal-Wallis H test for {column} by {group_column}:")
    print("======================================================================================================")
    print(f"H Stat: {stat}, p-value: {p_value}\n")
    return decision(p_value=p_value, sig_level=Sig_level)


def anova_test(df: pd.DataFrame, column:str ,group_column: list[str], Sig_level: float = 0.05) -> str:
    """
    Perform a one-way ANOVA on three or more independent groups.
    used when data is normally distributed
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    column(Str): variable to test 
    group_columnslist(str): The column name of the groups.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    """
    groups = [group[column].values for name, group in df.groupby(group_column)]
    stat, p_value = stats.f_oneway(*groups)
    print(f"One-way ANOVA for groups {column}:")
    print("======================================================================================================")
    print(f"F Stat: {stat}, p-value: {p_value}\n")
    return decision(p_value=p_value, sig_level=Sig_level)


def chi2_independence_test(df: pd.DataFrame, row_column: str, col_column: str, Sig_level: float = 0.05) -> str:
    """
    Perform a chi-square test of independence on three or more  categorical variables.
    used when data is not normally distributed and is categorical
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    row_column (str): The column name of the rows in the contingency table.
    col_column (str): The column name of the columns in the contingency table.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.

    Returns:
    str: Result of the decision function based on the p-value and significance level.
    """
    table = pd.crosstab(df[row_column], df[col_column])
    chi2_stat, p_value, dof, expected = stats.chi2_contingency(table)
    print(f"Chi-square test of independence for {row_column} and {col_column}:")
    print("======================================================================================================")
    print(f"Chi2 Stat: {chi2_stat}, p-value: {p_value}\n")
    return decision(p_value=p_value, sig_level=Sig_level)

##########  END OF THREE GROUP OR MORE  STATISTICAL TESTS #################################

################## Start of post hoc tests for independent groups #####################################

def pairwise_mannwhitneyu(df: pd.DataFrame, column: str, group_column: str, Sig_level: float = 0.05) -> None:
    """
    Perform pairwise Mann-Whitney U tests for post hoc analysis after the Kruskal-Wallis H test.
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    column (str): The column name of the variable.
    group_column (str): The column name of the groups.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.
    """
    groups = {name: group[column].values for name, group in df.groupby(group_column)}
    comparisons = list(itertools.combinations(groups.keys(), 2))
    for (group1, group2) in comparisons:
        stat, p_value = stats.mannwhitneyu(groups[group1], groups[group2])
        print(f"Mann-Whitney U test between {group1} and {group2}: U Stat: {stat}, p-value: {p_value}, Significant: {p_value < Sig_level/len(comparisons)}")


def tukey_hsd_posthoc(df: pd.DataFrame, column: str, group_column: str) -> None:
    """
    Perform Tukey HSD post hoc analysis after one-way ANOVA.
    
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    column (str): The column name of the variable.
    group_column (str): The column name of the groups.
    """
    comp = MultiComparison(df[column], df[group_column])
    post_hoc_res = comp.tukeyhsd()
    print(post_hoc_res)


def pairwise_chi2_test(df: pd.DataFrame, row_column: str, col_column: str, Sig_level: float = 0.05) -> None:
    """
    Perform pairwise chi-square tests for post hoc analysis after the chi-square test of independence.
    Null hypothesis : No difference

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    row_column (str): The column name of the rows in the contingency table.
    col_column (str): The column name of the columns in the contingency table.
    Sig_level (float, optional): The significance level for the test. Default is 0.05.
    """
    table = pd.crosstab(df[row_column], df[col_column])
    groups = table.columns
    comparisons = list(itertools.combinations(groups, 2))
    for (group1, group2) in comparisons:
        sub_table = table.loc[:, [group1, group2]]
        chi2_stat, p_value, dof, expected = stats.chi2_contingency(sub_table)
        print(f"Chi-square test between {group1} and {group2}: Chi2 Stat: {chi2_stat}, p-value: {p_value}, Significant: {p_value < Sig_level/len(comparisons)}")

################## End of post hoc tests for independent groups #####################################