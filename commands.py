import secrets
import subprocess


def can_you_dig_it(the_site):
    the_ips = []
    dig_it = subprocess.check_output(['dig', f'{the_site}', 'A', f'{the_site}', 'AAAA'],
                                     shell=False).decode()
    for each_line in dig_it.split(';; ANSWER SECTION:')[1:]:
        the_ips.append(each_line.split('\n\n')[0].strip('\n').split('\t')[-1])
    return ', '.join(the_ips)


def roll_dice(how_many_sides):
    the_dice = range(1, how_many_sides + 1)
    return secrets.choice(the_dice)
