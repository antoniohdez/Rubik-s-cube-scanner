my @colors = ('B','D','F','L','R','U');
my @numbers = (0,1,2,3,4,5,6,7,8);
my $counter = 1;
#my $med = B0.material.color = getColor(match.Groups[1].Value);

foreach my $col (@colors)
{
  foreach my $n (@numbers)
  {
    print "$col$n.material.color = getColor(match.Groups[$counter].Value);\n";
    $counter++;
  }
}

my $in = "{'B': [['O', 'O', 'O'], ['O', 'O', 'O'], ['G', 'G', 'G']], 'D': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']], 'F': [['B', 'B', 'B'], ['R', 'R', 'R'], ['R', 'R', 'R']], 'L': [['B', 'B', 'O'], ['B', 'B', 'O'], ['B', 'B', 'O']], 'R': [['R', 'G', 'G'], ['R', 'G', 'G'], ['R', 'G', 'G']], 'U': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]}";
$in =~ s/\w/\(\\w\)/g;
$in =~ s/(\[|\])/\\$1/g;
print "$in\n";
