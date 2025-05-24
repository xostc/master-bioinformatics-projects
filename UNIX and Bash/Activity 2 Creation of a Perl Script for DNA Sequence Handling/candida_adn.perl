#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';  # Habilito say para imprimir con salto de línea automático
use diagnostics;

# Procesar el archivo FASTA que contiene la secuencia de ADN

my $archivo_fasta = "Perl_candida.fasta";  # defino la variable $fasta_file que almacena el nombre del archivo FASTA a procesar, 
#en este caso "Perl_candida.fasta".

# Apertura archivo FASTA

open(my $fh, '<', $archivo_fasta) or die "No se pudo abrir el archivo '$archivo_fasta': $!\n"; #Abro el archivo en modo lectura ('<') y 
#asigno una variable $fh que lee el archivo de la variable antes designada $fasta_file con la secuencia.

my $header = <$fh>;  # Leo la primera línea (cabecera) que contiene información sobre la secuencia

chomp($header); # elimino el salto de línea final de esa línea leída, para que no quede un carácter extra al final.


my $secuencia = ""; # Creo una variable $sequence vacía que se usará para almacenar la secuencia de ADN.
while (my $line = <$fh>) { # leo cada línea del archivo y le asigno a la variable $line
    chomp($line);
    $secuencia .= $line;  # concateno cada línea (sin saltos de línea) a la variable $sequence para obtener la secuencia completa de ADN
}
close $fh;

# Me aseguro de que la secuencia esté en mayúsculas
$secuencia = uc($secuencia);

# Calculo la longitud de la secuencia de ADN
my $length = length($secuencia);
say "La longitud de la secuencia de ADN es: $length bases";

# Cuento el número de bases A, T, C, G en la secuencia
my $count_A = ($secuencia =~ tr/A//);
my $count_T = ($secuencia =~ tr/T//);
my $count_C = ($secuencia =~ tr/C//);
my $count_G = ($secuencia =~ tr/G//);
say "Conteo de bases:";
say "A: $count_A";
say "T: $count_T";
say "C: $count_C";
say "G: $count_G";

# Obtengo la secuencia complementaria de ADN
my $secuencia_complementaria = $secuencia;
$secuencia_complementaria =~ tr/ATCG/TAGC/;
say "La secuencia complementaria es:";
say $secuencia_complementaria;

# Busco el motivo GGGAGCAAT en la secuencia y muestro la posiciones
my $pos = 0; 
my $motif = "GGGAGCAAT";
say "\nBuscando el motivo '$motif' en la secuencia...";

my @posiciones;
while ($secuencia =~ /$motif/g) {
    # Calculando la posición del motivo (ajustando la posición al principio del motivo)
    $pos = pos($secuencia) - length($motif) + 1;
    push @posiciones, $pos;  # Almaceno la posición en el array
}

if (@posiciones) {
    say "Motivo encontrado en las posiciones: @posiciones";
} else {
    say "Motivo no encontrado en la secuencia.";
}


exit;
