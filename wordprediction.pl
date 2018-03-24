#!/usr/bin/perl
use strict;
use warnings;

use Tree::Suffix;

sub gen_data_structures {
    my $dict_filename = shift;
    my @words = read_file($dict_filename, chomp => 1);
    $tree = Tree::Suffix->new(@words);
}

sub get_suffixes {
    my $query = shift;
    @matches = $tree->search($query);
    return @matches;
}

gen_data_structures("words");

@suffixes = get_suffixes("comp");

print "$_\n" for @suffixes;
