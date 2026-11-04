from django.db import models

# Create your models here.


class Categorie(models.Model):
    class Meta:
        ordering = ['nume']
        verbose_name = "Categorie"
        verbose_name_plural = "Categorii"
        indexes = [
        models.Index(fields=['nume'], name='categorie_nume_idx'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(nume=''),
                name='categorie_nume_nevid',
                violation_error_message="Numele categoriei nu poate fi gol!"
            )
        ]
    nume = models.CharField( max_length=100, unique=True,
        error_messages={
            'unique': "Această categorie există deja!",
            'max_length': "Numele categoriei poate avea maximum 100 de caractere."
        }, help_text="Numele categoriei de flori."
    )
    culoare = models.CharField( max_length=50, null=True,  blank=True,
        help_text="Culoarea caracteristică florilor din această categorie."
    )
    descriere = models.TextField( null=True, blank=True,
        help_text="Descrierea categoriei și a caracteristicilor florilor incluse."
    )
    sezon = models.CharField( max_length=20,
        choices=[ ('primavara', 'Primăvara'),
            ('vara', 'Vara'),
            ('toamna', 'Toamna'),
            ('iarna', 'Iarna'),
            ('tot_anul', 'Tot anul')
        ], default='tot_anul', help_text="Sezonul natural asociat categoriei de flori."
    )
    sigla = models.ImageField( upload_to='categorii/', null=True, blank=True, help_text="Imagine reprezentativă pentru categoria de flori."
    )

    def __str__(self):
        return self.nume
    
    
class Floare(models.Model):
    class Meta:
        ordering = ['nume']
        verbose_name = "Floare"
        verbose_name_plural = "Flori"
        indexes = [
        models.Index(fields=['nume'], name='floare_nume_idx'),
        models.Index(fields=['pret'], name='floare_pret_idx'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(pret__gt=0),
                name='floare_pret_pozitiv',
                violation_error_message="Prețul florii trebuie să fie pozitiv!"
            ),
            models.CheckConstraint(
                condition=models.Q(durata_viata__gt=0),
                name='floare_durata_pozitiva',
                violation_error_message="Durata de viață trebuie să fie pozitivă!"
            )
        ]

    nume = models.CharField( max_length=100,
        error_messages={
            'max_length': "Numele florii poate avea maximum 100 de caractere." },
        help_text="Numele florii."
    )
    pret = models.DecimalField( max_digits=8, decimal_places=2, help_text="Prețul unei flori, exprimat în lei."
    )
    culoare = models.CharField( max_length=50, null=True, blank=True, help_text="Culoarea florii."
    )
    descriere = models.TextField( null=True, blank=True, help_text="Descrierea și caracteristicile florii."
    )
    durata_viata = models.PositiveIntegerField( help_text="Durata de viață estimată a florii, în zile."
    )
    producator = models.CharField( max_length=100, null=True, blank=True, help_text="Producătorul florii."
    )
    disponibilitate = models.BooleanField( default=True, help_text="Indică dacă floarea este disponibilă pentru comandă."
    )
    categorie = models.ForeignKey( Categorie,
        on_delete=models.PROTECT,
        related_name='flori',
        help_text="Categoria din care face parte floarea."
    )

    def __str__(self):
        return f"{self.nume} - {self.categorie} - {self.culoare}"
    
class Ambalaj(models.Model):
    class Meta:
        ordering = ['material']
        verbose_name = "Ambalaj"
        verbose_name_plural = "Ambalaje"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(marime__gt=0),
                name='ambalaj_marime_pozitiva',
                violation_error_message="Mărimea ambalajului trebuie să fie pozitivă!"
            )
        ]

    material = models.CharField( max_length=100, help_text="Materialul din care este realizat ambalajul."
    )
    marime = models.PositiveIntegerField( default=1, help_text="Mărimea ambalajului."
    )
    culoare = models.CharField( max_length=50, null=True, blank=True, help_text="Culoarea ambalajului."
    )

    def __str__(self):
        return f"{self.material} - {self.marime} - {self.culoare or 'fără culoare'}"

class Buchet(models.Model):
    class Meta:
        ordering = ['denumire']
        verbose_name = "Buchet"
        verbose_name_plural = "Buchete"
        indexes = [
        models.Index(fields=['pret'], name='buchet_pret_idx'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(pret__gt=0),
                name='buchet_pret_pozitiv',
                violation_error_message="Prețul buchetului trebuie să fie pozitiv!"
            )
        ]

    denumire = models.CharField( max_length=100, unique=True,
        error_messages={
            'unique': "Există deja un buchet cu această denumire!",
            'max_length': "Denumirea buchetului poate avea maximum 100 de caractere."
        }, help_text="Denumirea buchetului."
    )
    pret = models.DecimalField( max_digits=8, decimal_places=2, help_text="Prețul buchetului, exprimat în lei."
    )
    stil = models.CharField( max_length=50, null=True, blank=True, default='clasic', help_text="Stilul buchetului, de exemplu elegant sau rustic."
    )
    paleta_culori = models.CharField( max_length=100, null=True, blank=True, help_text="Paleta de culori folosită în buchet."
    )
    flori = models.ManyToManyField( Floare,
        related_name='buchete',
        help_text="Florile care intră în componența buchetului."
    ) 
    ambalaj = models.ForeignKey( Ambalaj,
    on_delete=models.PROTECT,
    related_name='buchete',
    help_text="Ambalajul folosit pentru buchet."
    )

    def __str__(self):
        return self.denumire
    

class TipEveniment(models.Model):
    class Meta:
        ordering = ['tip_eveniment']
        verbose_name = "Tip Eveniment"
        verbose_name_plural = "Tip Evenimente"
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(tip_eveniment=''),
                name='eveniment_tip_nevid',
                violation_error_message="Tipul evenimentului nu poate fi gol!"
            )
        ]

    tip_eveniment = models.CharField( max_length=100,unique=True,
        error_messages={
            'unique': "Acest tip de eveniment există deja!"
        }, help_text="Denumirea tipului de eveniment."
    )
    descriere = models.TextField( null=True, blank=True, help_text="Descrierea evenimentului."
    )
    tema = models.CharField( max_length=100, null=True, blank=True, help_text="Tema asociată evenimentului."
    )

    buchete = models.ManyToManyField( Buchet,
        related_name='tipuri_eveniment',
        help_text="Buchetele potrivite pentru acest tip de eveniment."
    )

    def __str__(self):
        return self.tip_eveniment
    

class RevistaSezoniera(models.Model):
    class Meta:
        ordering = ['numar_editie']
        verbose_name = "Revistă Sezonieră"
        verbose_name_plural = "Reviste Sezoniere"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(numar_editie__gt=0),
                name='revista_numar_editie_pozitiv',
                violation_error_message="Numărul ediției trebuie să fie pozitiv!"
            ),
            models.UniqueConstraint(
                fields=['categorie', 'numar_editie'],
                name='revista_categorie_editie_unica'
            )
        ]

    categorie = models.ForeignKey( Categorie,
        on_delete=models.PROTECT,
        related_name='reviste',
        help_text="Categoria Sezon asociată revistei."
    )
    numar_editie = models.PositiveIntegerField( help_text="Numărul ediției revistei."
    )
    titlu = models.CharField( max_length=150,
        error_messages={
        'max_length': "Titlul revistei poate avea maximum 150 de caractere."
        },
        help_text="Titlul revistei sezoniere."
    )
    sezon = models.CharField(
    max_length=20,
    choices=[('primavara', 'Primăvara'),
        ('vara', 'Vara'),
        ('toamna', 'Toamna'),
        ('iarna', 'Iarna')
    ],
    help_text="Alege anotimpul pe care îl prezintă revista."
    )
    data_publicare = models.DateTimeField(
    auto_now_add=True,
    help_text="Data și ora publicării revistei."
    )

    def __str__(self):
        return f"{self.titlu} - ediția {self.numar_editie}"




