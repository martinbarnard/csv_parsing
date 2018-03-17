# -*- coding: utf-8 -*-

import bink
import pytest
from unittest.mock import patch #, mock_open

def test_args_happy_path():
    '''
    Pytest for the happy path args
    '''
    args = ['--file' , 'bink/poles.csv']
    parser = bink.parse_args()
    nargs = parser.parse_args(args)
    assert(nargs.file == 'bink/poles.csv')

def test_args_years():
    args = ['-y']
    parser = bink.parse_args()
    nargs = parser.parse_args(args)
    assert(nargs.years == True)

def test_args_invalid(capsys):
    args = ['-a', 'what is this']
    with pytest.raises(SystemExit):
        parser = bink.parse_args()
        parser.parse_args(args)
        out, err = capsys.readouterr()
        assert out == 2

data="test,a,new,file"
# mock_open_func = mock_open(read_data=data)
def mock_csv(f):
    print('I was called with {}'.format(f))
    return [ {'this':123, 'is':'boo', 'a':123,'dict':'really?'} ]

@patch('bink.Pole')
def test_file_open(mockPole):
    '''
    Will have to mock the filesystem for reading.
    '''
    test_data = [
        {'a':12, 'b':23, 'c':'elephant'},
        {'a':12, 'b':23, 'c':'elephant'},
        {'a':12, 'b':23, 'c':'elephant'},
        {'a':12, 'b':23, 'c':'elephant'},
    ]
    pole = mockPole()
    pole.read_data.return_value = True
    pole.csv_data = test_data

    res = pole.read_data('test')
    assert res == True

@patch('bink.csv.DictReader', side_effect=mock_csv)
def test_csv_reader(mock_csv):
    pole=bink.Pole('f')
    assert pole.csv_data == [ {'this':123, 'is':'boo', 'a':123,'dict':'really?'} ]


