'''
user-facing functionality
'''

# if any new functions are added to create.py, you need to add them here.
__all__ =  ['seq_fractions', 'sequence', 'minimal_var', 'new_seq_constant_class_var', 'new_var', 'constant_class_var', 'constant_class_hydro_var', 'constant_residue_var', 'shuffle_var', 'kappa_var', 'alpha_helix', 'beta_strand', 'beta_sheet']

import os
import sys

#for sequence generation
from goose.backend.sequence_generation import generate_disordered_seq_by_fractions as _generate_disordered_seq_by_fractions
from goose.backend.sequence_generation import generate_disordered_seq_by_props as _generate_disordered_seq_by_props

# goose tools for checking and fixing parameters
from goose.backend.goose_tools import check_and_correct_props_kwargs as _check_and_correct_props_kwargs
from goose.backend.goose_tools import check_props_parameters as _check_props_parameters
from goose.backend.goose_tools import check_and_correct_fracs_kwargs as _check_and_correct_fracs_kwargs
from goose.backend.goose_tools import check_fracs_parameters as _check_fracs_parameters
from goose.backend.goose_tools import length_check as _length_check

# variant generation stuff
from goose.backend.variant_generation import gen_kappa_variant as _gen_kappa_variant
from goose.backend.variant_generation import gen_shuffle_variant as _gen_shuffle_variant
from goose.backend.variant_generation import gen_constant_residue_variant as _gen_constant_residue_variant
from goose.backend.variant_generation import gen_hydropathy_class_variant as _gen_hydropathy_class_variant
from goose.backend.variant_generation import gen_new_variant as _gen_new_variant
from goose.backend.variant_generation import gen_constant_class_variant as _gen_constant_class_variant
from goose.backend.variant_generation import gen_new_var_constant_class as _gen_new_var_constant_class
from goose.backend.gen_minimal_variant_backend import gen_minimal_sequence_variant as _gen_minimal_sequence_variant

# for folded structure generation
from goose.backend.folded_region_generation import gen_helix as _gen_helix
from goose.backend.folded_region_generation import gen_beta_strand as _gen_beta_strand
from goose.backend.folded_region_generation import gen_beta_sheet as _gen_beta_sheet

# FOR WHEN THINGS GO WRONG
from goose import goose_exceptions

# because every good package needs some parameters
from goose.backend import parameters

#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/             \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/  Create     \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/  sequence   \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/  By         \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/  Specifying \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/  Properties \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/             \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-

def sequence(length, **kwargs):
    """
    Stand alone function that takes care of creating sequences with specified
    properties. Takes in various sequence parameters as arguments. 

    Parameters
    ------------
    length : Int
        length of desired disordered sequence
    **kwargs : parameter and parameter value
        Takes in possible parameters for GOOSE. Possible parameters/parameter combinations are:
            FCR : Float
                specify the fraction of charged residues (between 0 and 1)
            NCPR : Float 
                specify the net charge per residue of generated sequences (between -1 and 1)
            sigma : Float
                specify the sigma value of generated sequences(between 0 and 1)
            hydro : float 
                specify the mean hydropathy of generated sequences
            kappa : float
                specify the kappa value of generated seqeunces
            cutoff : Float
                the disorder cutoff threshold
            **Note** can specify NCPR and FCR simultaneously
                     can specify NCPR and FCR and hydro simultaneously


    Returns
    -----------
    generated_seq : String
        Returns a string that is the amino acid sequence

    """
    # check length
    _length_check(length)

    # First correct kwargs. Do this first because
    # the next function that looks over kwargs values
    # can only take in corrected kwargs.
    kwargs = _check_and_correct_props_kwargs(**kwargs)

    # now make sure that the input vals are within appropriate bounds
    _check_props_parameters(**kwargs)

    # make sure length is within bounds
    if length > parameters.MAXIMUM_LENGTH:
        error_message = f'length of {length} is greater than maximum allowed value of {parameters.MAXIMUM_LENGTH}'
        raise goose_exceptions.GooseInputError(error_message)
    if length < parameters.MINIMUM_LENGTH:
        error_message = f'length of {length} is less than maximum allowed value of {parameters.MINIMUM_LENGTH}'
        raise goose_exceptions.GooseInputError(error_message)

    # make the sequence
    try:
        generated_seq = _generate_disordered_seq_by_props(length, FCR=kwargs['FCR'], NCPR=kwargs['NCPR'], hydropathy=kwargs['hydropathy'],
            sigma = kwargs['sigma'], attempts = 1, allowed_hydro_error = parameters.HYDRO_ERROR, disorder_threshold = kwargs['cutoff'])
    except:
        raise goose_exceptions.GooseFail('Unable to generate sequence. Please try again with different parameters or a lower cutoff value.')

    # this is a bit hacky for now, but it works.
    if kwargs['kappa'] != None:
        try:
            generated_seq = _gen_kappa_variant(generated_seq, kappa=kwargs['kappa'], allowed_kappa_error = parameters.MAXIMUM_KAPPA_ERROR, disorder_threshold=kwargs['cutoff'], strict_disorder=False)
        except:
            raise goose_exceptions.GooseFail('Unable to get kappa of generated sequence correct')
    # return the seq
    return generated_seq


#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/             \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/  Create     \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/  sequence   \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/  By         \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/  Specifying \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/  Fractions  \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/             \|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-
#-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-


def seq_fractions(length, **kwargs):
    """
    Stand alone function that takes care of creating sequences with specified
    fractions of amino acids. 

    Parameters
    ------------
    length : Int
        length of desired disordered sequence
    **kwargs : parameter and parameter value
        Takes in amino acids followed by the fraction value as a decimal.


    Returns
    -----------
    generated_seq : String
        Returns a string that is the amino acid sequence

    """
    # check length
    _length_check(length)

    # First correct kwargs. Do this first because
    # the next function that looks over kwargs values
    # can only take in corrected kwargs.
    kwargs = _check_and_correct_fracs_kwargs(**kwargs)

    # now make sure that the input vals are within appropriate bounds
    _check_fracs_parameters(**kwargs)

    # make sure length is within bounds
    # length is the only thing not checked by my check / check and correct functions.
    if length > parameters.MAXIMUM_LENGTH:
        error_message = f'length of {length} is greater than maximum allowed value of {parameters.MAXIMUM_LENGTH}'
        raise goose_exceptions.GooseInputError(error_message)
    if length < parameters.MINIMUM_LENGTH:
        error_message = f'length of {length} is less than maximum allowed value of {parameters.MINIMUM_LENGTH}'
        raise goose_exceptions.GooseInputError(error_message)

    generated_seq = _generate_disordered_seq_by_fractions(length, **kwargs)

    # return the seq
    return generated_seq


'''
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
          VARIANT GENERATORS
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
'''



def minimal_var(input_sequence, hydropathy = '', fcr = '', 
    ncpr = '', scd='', cutoff=parameters.DISORDER_THRESHOLD, strict=False):
    '''
    User facing function for generating the minimal sequence variant. This variant
    tries to make a sequence as similar to the input sequence as possible all while
    minimizing the number of amino acids changed. 
    '''
    # check length
    _length_check(input_sequence)

    if cutoff > 1 or cutoff < 0:
        raise goose_exceptions.GooseInputError('cutoff value must be between 0 and 1 for disorder threshold')    
    try:
        final_sequence = _gen_minimal_sequence_variant(input_sequence, mean_hydro = hydropathy, fraction = fcr, 
        net_charge = ncpr, charge_asymmetry=scd, cutoff=cutoff, strict=strict)
    except:
        raise goose_exceptions.GooseFail('Sorry! GOOSE was unable to generate the sequence. Please try again or try with different parameters or a lower cutoff value.')
    return final_sequence



def new_seq_constant_class_var(sequence,
    cutoff = parameters.DISORDER_THRESHOLD, strict=False):
    '''
    A function to generate a variant where the sequence composition is new but
    the numbers of each residue from each class is the same. The overall properties
    of the generated sequence will also be constant.
    '''
    # check length
    _length_check(sequence)

    if cutoff > 1 or cutoff < 0:
        raise goose_exceptions.GooseInputError('cutoff value must be between 0 and 1 for disorder threshold')
    try:
        final_sequence = _gen_new_var_constant_class(sequence, disorder_threshold=cutoff, strict_disorder=strict)
    except:
        raise goose_exceptions.GooseFail('Sorry! GOOSE was unable to generate the sequence. Please try again or try with a lower cutoff value.')
    return final_sequence



def constant_class_var(sequence,
    cutoff = parameters.DISORDER_THRESHOLD, strict=False):
    '''
    function to generate a variant with the same properties as the 
    input variant as well as the same order of amino acids as
    far as class and the same number in each class
    '''
    # check length
    _length_check(sequence)

    if cutoff > 1 or cutoff < 0:
        raise goose_exceptions.GooseInputError('cutoff value must be between 0 and 1 for disorder threshold')    
    try:
        final_sequence = _gen_constant_class_variant(sequence, disorder_threshold=cutoff, strict_disorder=strict)
    except:
        raise goose_exceptions.GooseFail('Sorry! GOOSE was unable to generate the sequence. Please try again or try with a lower cutoff value.')
    return final_sequence


def new_var(sequence,
    cutoff = parameters.DISORDER_THRESHOLD, strict=False):
    '''
    function to generate a variant that is completely different
    in sequence to the input but has all the same overall parameters.
    Does not account for specific classes of residues.
    '''
    # check length
    _length_check(sequence)

    if cutoff > 1 or cutoff < 0:
        raise goose_exceptions.GooseInputError('cutoff value must be between 0 and 1 for disorder threshold')    
    try:
        final_sequence = _gen_new_variant(sequence, disorder_threshold=cutoff, strict_disorder=strict)
    except:
        raise goose_exceptions.GooseFail('Sorry! GOOSE was unable to generate the sequence. Please try again or try with a lower cutoff value.')
    return final_sequence


def constant_class_hydro_var(sequence, hydropathy, hydro_error = parameters.HYDRO_ERROR,
    cutoff = parameters.DISORDER_THRESHOLD, strict=False):
    '''
    function to take in a sequence and make a variant that adjusts the
    hydropathy while keeping the position and number of amino acids the
    same by class of amino acid
    '''

    # check length
    _length_check(sequence)

    if cutoff > 1 or cutoff < 0:
        raise goose_exceptions.GooseInputError('cutoff value must be between 0 and 1 for disorder threshold')    
    try:
        final_sequence = _gen_hydropathy_class_variant(sequence, hydropathy=hydropathy, allowed_hydro_error = hydro_error, disorder_threshold=cutoff, strict_disorder=strict)
    except:
        raise goose_exceptions.GooseFail('Sorry! GOOSE was unable to generate the sequence. Please try again or try with a lower cutoff value.')
    return final_sequence




def constant_residue_var(sequence, constant=[], 
    cutoff = parameters.DISORDER_THRESHOLD, strict=False):
    '''
    function that will generate a new sequence variant
    where specific residues are held constant. The 
    variant will have the same aggregate properties
    as the original sequence.
    '''
    # check length
    _length_check(sequence)

    if cutoff > 1 or cutoff < 0:
        raise goose_exceptions.GooseInputError('cutoff value must be between 0 and 1 for disorder threshold')
    try:
        final_sequence = _gen_constant_residue_variant(sequence, constant_residues=constant, disorder_threshold=cutoff, strict_disorder=strict)
    except:
        raise goose_exceptions.GooseFail('Sorry! GOOSE was unable to generate the sequence. Please try again or try with a lower cutoff value or with different constant residues.')
    return final_sequence



def shuffle_var(sequence, shuffle=[], 
    cutoff = parameters.DISORDER_THRESHOLD, strict=False):
    '''
    Function that will shuffle specific regions of an IDR.
    Multiple regions can be specified simultaneously.
    '''
    # check length
    _length_check(sequence)

    if cutoff > 1 or cutoff < 0:
        raise goose_exceptions.GooseInputError('cutoff value must be between 0 and 1 for disorder threshold')    

    all_vals = []
    if shuffle != []:
        for val in shuffle:
            if type(val) == list:
                for subval in val:
                    all_vals.append(subval)
            else:
                all_vals.append(val)
    
    for val in all_vals:
        if val < 1:
            raise goose_exceptions.GooseInputError('Cannot have a value to shuffle below 1')
        if val > len(sequence):
            raise goose_exceptions.GooseInputError('Cannot specify to shuffle a region greater than the length of your sequence')

    curvals = []
    if type(shuffle[0])==list:
        if len(shuffle) >= 2:
            for sublist in shuffle:
                for i in range(sublist[0], sublist[1]+1):
                    if i in curvals:
                        raise goose_exceptions.GooseInputError('Cannot have overlapping regions to shuffle.')
                    else:
                        curvals.append(i)

    try:
        final_sequence = _gen_shuffle_variant(sequence, shuffle_regions=shuffle, disorder_threshold=cutoff, strict_disorder=strict)
    except:
        raise goose_exceptions.GooseFail('Sorry! GOOSE was unable to generate the sequence. Please try again or try with a lower cutoff value or with different constant residues.')
    return final_sequence




def kappa_var(sequence, kappa, kappa_error=parameters.MAXIMUM_KAPPA_ERROR, 
    cutoff=parameters.DISORDER_THRESHOLD, strict=False):
    '''
    Function to generate a sequence with a user-defined
    kappa value. Requires kappa calculation using 
    SPARROW. Kappa is a function of charge asymmetry, larger
    kappa values have more asymmetrically distributed
    charged residues.
    '''
    # check length
    _length_check(sequence)

    if cutoff > 1 or cutoff < 0:
        raise goose_exceptions.GooseInputError('cutoff value must be between 0 and 1 for disorder threshold')    
    if len(sequence) < 6:
        raise GooseInputError('Cannot have sequence with a length less than 6')
    if kappa > 1 or kappa < 0:
        raise GooseInputError('Kappa values must be between 0 and 1')

    try:
        final_sequence = _gen_kappa_variant(sequence, kappa=kappa, allowed_kappa_error = kappa_error, disorder_threshold=cutoff, strict_disorder=strict)
    except:
        raise goose_exceptions.GooseFail('Sorry! GOOSE was unable to generate the sequence. Please try again or try with a lower cutoff value or with different kappa value')
    return final_sequence


'''
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
 PREDICTED FOLDED REGION GENERATORS
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
'''


from goose.backend.folded_region_generation import gen_helix as _gen_helix
from goose.backend.folded_region_generation import gen_beta_strand as _gen_beta_strand
from goose.backend.folded_region_generation import gen_beta_sheet as _gen_beta_sheet


def alpha_helix(length):
    '''
    user facing function for generating a sequence predicted to be an alpha
    helix based on DSSP scores.
    '''
    if length > 150:
        raise goose_exceptions.GooseInputError('Unable to make alpha helix with length greater than 150.')    
    elif length < 8:
        raise goose_exceptions.GooseInputError('Unable to make alpha helix with length less than 8.')    
    else:
        try:
            final_seq = _gen_helix(length)
        except:
            raise goose_exceptions.GooseFail('Sorry! Goose was unable to make that helix. Try again or try a different length.')
        return final_seq


def beta_strand(length):
    '''
    user facing function for generating a sequence predicted to be 
    a beta strand based on DSSP scores.
    '''
    if length > 34:
        raise goose_exceptions.GooseInputError('Unable to make beta strands with length greater than 34.')
    elif length < 5:
        raise goose_exceptions.GooseInputError('Unable to make beta strands with length less than 5.')
    else:
        try:
            final_seq = _gen_beta_strand(length)
        except:
            raise goose_exceptions.GooseFail('Sorry! Goose was unable to make that strand. Try again or try a different length.')
        return final_seq



def beta_sheet(length):
    '''
    user facing function for generating a sequence predicted to be 
    a beta sheet based on DSSP scores. uses coils to connect strands.
    '''
    if length < 18:
        raise goose_exceptions.GooseInputError('cannot generate beta sheet less than 18 amino acids.')
    elif length > 400:
        raise goose_exceptions.GooseInputError('cannot generate beta sheet greater than 400 amino acids.')
    try:
        final_seq = _gen_beta_sheet(length)
    except:
        raise goose_exceptions.GooseFail('Sorry! Goose was unable to make that beta sheet. Try again or try a different length.')
    return final_seq


