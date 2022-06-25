'''
various tools for GOOSE
'''


'''
various essential tools to help GOOSE take flight
'''
import random
from random import randint

import csv

from goose.goose_exceptions import GooseError, GooseInputError

from goose.backend import parameters

from goose.backend.sequence_generation_backend import calculate_max_charge


def length_check(input_val):
    '''
    function to make sure length parameters don't go out of bounds
    '''
    if type(input_val) == str:
        length = len(input_val)
    elif type(input_val) == int:
        length = input_val
    else:
        raise GooseError('length check function in goose tools got an input value not string or int.')

    if length > parameters.MAXIMUM_LENGTH or length < parameters.MINIMUM_LENGTH:
        error_message = f'\nLength of {length} is not within the allowed range for length of between {parameters.MINIMUM_LENGTH} and {parameters.MAXIMUM_LENGTH}'
        raise GooseInputError(error_message)


def write_csv(input_list, output_file, properties):
    """
    Function that writes the scores in an input dictionary out to a standardized CVS file format.

    Parameters
    -----------
    input_list : List
        List of dictionaries

    output_file : str
        Location and filename for the output file. Assumes .csv is provided.

    properties : Bool
        Whether or not to save the sequence properties. 

        If True
            save an autogenerated sequence name, length, the FCR, NCPR, hydropathy,
            sigma, delta values, fractions of the sequence followed by the sequence.

        If false
            just saves the sequence

    Returns
    --------
    None
        No return value, but writes a .csv file to disk

    """

    header_names=[]

    if properties == True:
        for header, values in input_list[0].items():
            header_names.append(header)
    
    else:
        # if properties was false, input_list is not a list of dicts
        # but rather a list of strings (the seqeunces). Need to make
        # into a list of dicts and give each sequence a name!
        amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
        final_list = []
        header_names = ['Name', 'sequence']
        for sequence in input_list:
            temp_dict = {}
            seq_name = '>'        
            for i in range(0, 5):
                seq_name += amino_acids[random.randint(0, len(amino_acids)-1)]
                seq_name += str(random.randint(0, 9))
            temp_dict['Name'] = seq_name
            temp_dict['sequence'] = sequence
            final_list.append(temp_dict)

    # try and open the file and throw exception if anything goes wrong    
    try:    
        with open(output_file, 'w', newline='') as csvfile:
            writer=csv.DictWriter(csvfile, fieldnames=header_names)
            writer.writeheader()
            if properties == True:
                for i in input_list:
                    writer.writerow(i)

            else:
                for i in final_list:
                    writer.writerow(i)

    except Exception:
            raise GooseError('Unable to write to file destination %s' % (output_file))                  







def remove_None(**kwargs):
    '''
    function to remove none values from kwargs to make the CLI work
    make a list to keep track of kwargs to remove because can't remove
    during iteration as it changes the dictionary length
    '''

    remove_from_kwargs = []
    for i in kwargs.keys():
        if (kwargs[i]) == None:
           remove_from_kwargs.append(i)

    # for everything identified as None, remove it form kwargs
    for i in remove_from_kwargs:
        del kwargs[i]

    return kwargs


def check_props_parameters(**kwargs):
    '''
    function that makes sure the values for a given seq are not 
    outside possible bounds. Only for generating
    sequences by specifying properties.
    '''

    # check disorder disorder cutoff value bounds
    if 'cutoff' in list(kwargs.keys()):
        curval = kwargs['cutoff']
        if curval != None:
            if curval > parameters.MAXIMUM_DISORDER:
                error_message = f'The disorder cutoff value {curval} is greater than the max allowed value of {parameters.MAXIMUM_DISORDER}'
                print(error_message)
                raise GooseInputError(error_message)
            if curval < parameters.MINIMUM_DISORDER:
                error_message = f'The disorder cutoff {curval} is less than the minimum allowed value of {parameters.MINIMUM_DISORDER}'
                raise GooseInputError(error_message)

    # check FCR bounds
    if kwargs['FCR'] != None:
        curval = kwargs['FCR']
        if curval > parameters.MAXIMUM_FCR:
            error_message = f'The FCR value {curval} is greater than the allowed value of {parameters.MAXIMUM_FCR}'
            raise GooseInputError(error_message)
        if curval < parameters.MINIMUM_FCR:
            error_message = f'The FCR value {curval} is less than the allowed value of {parameters.MINIMUM_FCR}'
            raise GooseInputError(error_message)

    # check NCPR bounds
    if kwargs['NCPR'] != None:
        curval = kwargs['NCPR']
        if curval > parameters.MAXIMUM_NCPR:
            error_message = f'The NCPR value {curval} is greater than the allowed value of {parameters.MAXIMUM_NCPR}'
            raise GooseInputError(error_message)
        if curval < parameters.MINIMUM_NCPR:
            error_message = f'The NCPR value {curval} is less than the allowed value of {parameters.MINIMUM_NCPR}'
            raise GooseInputError(error_message)

    # check hydropathy bounds
    if kwargs['hydropathy'] != None:
        curval = kwargs['hydropathy']
        if curval > parameters.MAXIMUM_HYDRO:
            error_message = f'The hydropathy value {curval} is greater than the allowed value of {parameters.MAXIMUM_HYDRO}'
            raise GooseInputError(error_message)
        if curval < parameters.MINIMUM_HYDRO:
            error_message = f'The hydropathy value {curval} is less than the allowed value of {parameters.MINIMUM_HYDRO}'
            raise GooseInputError(error_message)

    # check sigma bounds
    if kwargs['sigma'] != None:
        curval = kwargs['sigma']
        if curval > parameters.MAXIMUM_SIGMA:
            error_message = f'The sigma value {curval} is greater than the allowed value of {parameters.MAXIMUM_SIGMA}'
            raise GooseInputError(error_message)
        if curval < parameters.MINIMUM_SIGMA:
            error_message = f'The sigma value {curval} is less than the allowed value of {parameters.MINIMUM_SIGMA}'
            raise GooseInputError(error_message)

    # make sure if sigma is specified, only sigma is specified
    if kwargs['sigma'] != None:
        # make list of other kwargs that can't be addiitonally specified.
        forbidden_sigma_kwargs = ['hydropathy', 'FCR', 'NCPR']
        # iterate through forbiddine kwargs
        for forbidden_kwarg in forbidden_sigma_kwargs:
            if kwargs[forbidden_kwarg] != None:
                error_message = f'If you specify sigma, you cannot specific FCR, hydropathy, or NCPR. You specified {kwargs[forbidden_kwarg]} in addition to sigma.'
                raise GooseInputError(error_message)

    # check FCR and NPCR error
    if kwargs['NCPR'] != None and kwargs['FCR'] != None:
        if abs(kwargs['NCPR']) > kwargs['FCR']:
            valncpr = kwargs['NCPR']
            valfcr = kwargs['FCR']
            error_message = f'The NCPR value of {valncpr} is not possible given the FCR value of {valfcr}'
            raise GooseInputError(error_message)

    # check kappa
    if kwargs['kappa'] != None:
        val_kappa = kwargs['kappa']
        if kwargs['kappa'] > 1:
            error_message = f'The kappa value of {val_kappa} is not possible. Values are between 0 and 1'
            raise GooseInputError(error_message)
        if kwargs['kappa'] < 0:
            error_message = f'The kappa value of {val_kappa} is not possible. Values are between 0 and 1'
            raise GooseInputError(error_message)        

    # check kappa based on FCR stuff
    if kwargs['kappa'] != None:
        if kwargs['FCR'] == 0:
            raise GooseInputError('Cannot specifiy kappa values when FCR is 0.')
        if kwargs['FCR'] != None:
            if kwargs['NCPR'] != None:
                if kwargs['NCPR'] == kwargs['FCR']:
                    raise GooseInputError('Cannot have NCPR = FCR for kappa to be a value other than -1.')


    # now check for charge AND hydro
    if kwargs['NCPR'] != None and kwargs['hydropathy'] != None:
        hydro_and_charge = True
    elif kwargs['FCR'] != None and kwargs['hydropathy'] != None:
        hydro_and_charge = True
    else:
        hydro_and_charge = False

    # get the charge value to use as the val for
    # checking hydro + charge errors
    if hydro_and_charge == True:
        if kwargs['FCR'] == None:
            check_charge_val = abs(kwargs['NCPR'])
        else:
            check_charge_val = kwargs['FCR']

        # now calculate maximum charge value
        max_possible_charge_value = calculate_max_charge(kwargs['hydropathy'])
        # now see if charge value used is within bounds
        if check_charge_val > max_possible_charge_value:
            curhydro = kwargs['hydropathy']
            error_message = f'The specified hydropathy value if {curhydro} is not compatible with the specified charge value.'
            raise GooseInputError(error_message)



def check_and_correct_props_kwargs(**kwargs):
    '''
    Checks the kwargs for creating a sequence by
    properties.
    
    Parameters
    -----------
    **kwargs : Dict
        The input dict to evaluate for completion and errors

    Returns
    -------
    Dict
        A dictionary holding all necessary (and corrected) 
        values for sequence generation.
    '''
    # first remove any 'None' arguments passed from the command line
    # from the kwargs dict.
    kwargs = remove_None(**kwargs)

    # list of possible FCR inputs
    possible_FCR = ['FCR', 'fcr', 'fCR', 'FcR', 'FCr', 'fcR', 'Fcr', 'fCr', 'fraction', 'fractoin', 'Fraction', 'Fractoin']

    # list of possible NCPR inputs
    possible_NCPR = ['NCPR', 'net_charge', 'net', 'Net_charge', 'net_Charge', 'Net', 'ncpr', 'nCPR', 'NcPR', 'NCpR', 'NCPr', 'ncPR', 'NcpR', 'NCpr', 'nCPr']

    # list of possible hydropathy inputs
    possible_hydro = ['hydropathy', 'mean_hydro', 'hydro', 'hydropath', 'mean_hydropathy', 'Mean_hydro', 'mean_Hydro', 'Mean_Hydro', 'Hydropathy', 'Hydro']

    # list of possible cutoff value inputs
    possible_cutoff = ['cutoff', 'cut', 'cut_off', 'cutoff_val', 'cutoff_value', 'Cutoff', 'Cut', 'Cut_Off', 'Cutoff_Val', 'Cutoff_val', 'cutoff_Value']

    # possible sigma values
    possible_sigma = ['sigma', 'Sigma', 'sigma_value', 'Sigma_value', 'Sigma_Value']

    # possible kappa values
    possible_kappa=['kappa', 'Kappa']

    # amino acid values
    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    lower_amino_acids = ['a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y']

    # make a list of all possible kwargs
    all_possible_kwargs = [possible_FCR, possible_NCPR, possible_hydro, possible_cutoff, possible_sigma, possible_kappa]

    # make an empty return kwarg dict
    return_kwarg = {}


    # iterate through all possible kwargs
    for individual_kwarg in kwargs.keys():
        for possible_kwarg in all_possible_kwargs:
            for possible_value in possible_kwarg:
                if individual_kwarg == possible_value:
                    correct_kwarg_key = possible_kwarg[0]
                    return_kwarg[correct_kwarg_key] = kwargs[individual_kwarg]

    # make list of various essential kwargs
    essential_kwargs = ['FCR', 'NCPR', 'hydropathy', 'sigma', 'cutoff', 'kappa']

    # make a dict of essential kwarg values
    essential_kwarg_vals = {'cutoff': parameters.DISORDER_THRESHOLD,'FCR': None, 'NCPR': None, 'hydropathy': None, 'sigma': None, 'kappa': None}

    # make sure essential_kwargs are in the final return kwarg
    for individual_kwarg in essential_kwargs:
        if individual_kwarg not in return_kwarg.keys():
            return_kwarg[individual_kwarg] = essential_kwarg_vals[individual_kwarg]

    # return the corrected dict
    return return_kwarg




def check_and_correct_fracs_kwargs(**kwargs):
    '''
    Checks the kwargs for creating a sequence by
    fractions.
    
    Parameters
    -----------
    **kwargs : Dict
        The input dict to evaluate for completion and errors

    Returns
    -------
    Dict
        A dictionary holding all necessary (and corrected) 
        values for sequence generation.
    '''
    # first remove any 'None' arguments passed from the command line
    # from the kwargs dict.
    kwargs = remove_None(**kwargs)

    # amino acid values
    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    lower_amino_acids = ['a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y']

    # list of all possible kwargs
    all_possible_kwargs = [amino_acids, lower_amino_acids]

    # make an empty return kwarg dict
    return_kwarg = {}

    # iterate through all possible kwargs, makes everything uppercase
    for individual_kwarg in kwargs.keys():
        for possible_kwarg in all_possible_kwargs:
            for possible_value in possible_kwarg:
                if individual_kwarg == possible_value:
                    correct_kwarg_key = individual_kwarg.upper()
                    return_kwarg[correct_kwarg_key] = kwargs[individual_kwarg]


    # list of essential kwargs, can add more here if needed
    essential_kwargs = ['cutoff', 'strict_disorder', 'attempts']

    # make a dict of essential kwarg values
    essential_kwarg_vals = {'cutoff': parameters.DISORDER_THRESHOLD, 'strict_disorder': False, 'attempts': 1}

    # make sure essential_kwargs are in the final return kwarg
    for individual_kwarg in essential_kwargs:
        if individual_kwarg not in return_kwarg.keys():
            return_kwarg[individual_kwarg] = essential_kwarg_vals[individual_kwarg]

    # return the corrected dict
    return return_kwarg


def check_fracs_parameters(**kwargs):
    '''
    function that makes sure the values for a given seq are not 
    outside possible bounds. Only for generating
    sequences by specifying fractions of amino acids.
    '''

    # check disorder disorder cutoff value bounds
    if 'cutoff' in list(kwargs.keys()):
        curval = kwargs['cutoff']
        if curval != None:
            if curval > parameters.MAXIMUM_DISORDER:
                error_message = f'The disorder cutoff value {curval} is greater than the max allowed value of {parameters.MAXIMUM_DISORDER}'
                print(error_message)
                raise GooseInputError(error_message)
            if curval < parameters.MINIMUM_DISORDER:
                error_message = f'The disorder cutoff {curval} is less than the minimum allowed value of {parameters.MINIMUM_DISORDER}'
                raise GooseInputError(error_message)

    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

    # make sure amino acids are within possible values
    for individual_kwargs in kwargs.keys():
        if individual_kwargs.upper() in amino_acids:
            # get current fraction value
            current_value = kwargs[individual_kwargs]
            # get max fraction value
            max_value = parameters.MAX_FRACTION_DICT[individual_kwargs.upper()]
            # make sure that current value not greater than max value
            if current_value > max_value:
                error_message = f'Current value of {current_value} is greater than max possible fraction value for amino acid {individual_kwargs.upper()}. Max value is {max_value}.'
                raise GooseInputError(error_message)









