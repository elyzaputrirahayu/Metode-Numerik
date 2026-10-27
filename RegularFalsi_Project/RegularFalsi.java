import java.util.Scanner;

public class RegularFalsi {
    interface Fungsi { double hitung(double x); }

    static Fungsi pilih(int n) {
        switch (n) {
            case 1: return x -> x*x*x - x - 2;
            case 2: return x -> x*x - 4;
            case 3: return x -> Math.cos(x) - x;
            case 4: return x -> Math.exp(x) - 3*x;
            case 5: return x -> x*x - x - 2;
            default: throw new IllegalArgumentException("Pilihan fungsi harus 1 sampai 5.");
        }
    }

    static double regulaFalsi(Fungsi f, double a, double b, double tol, int maks) {
        double fa=f.hitung(a), fb=f.hitung(b);
        if (fa==0) return a;
        if (fb==0) return b;
        if (!Double.isFinite(fa)||!Double.isFinite(fb)||fa*fb>0)
            throw new IllegalArgumentException("f(a) dan f(b) harus berlainan tanda.");
        double sebelumnya=Double.NaN, xr=Double.NaN;
        System.out.printf("%n%-5s %-12s %-12s %-12s %-12s%n","Iter","a","b","xr","f(xr)");
        for(int i=1;i<=maks;i++){
            if(Math.abs(fb-fa)<1e-15) throw new ArithmeticException("Penyebut mendekati nol.");
            xr=(a*fb-b*fa)/(fb-fa);
            double fr=f.hitung(xr);
            double galat=Double.isNaN(sebelumnya)?Double.NaN:Math.abs(xr-sebelumnya);
            System.out.printf("%-5d %-12.6f %-12.6f %-12.6f %-12.6f%n",i,a,b,xr,fr);
            if(Math.abs(fr)<=tol||(!Double.isNaN(galat)&&galat<=tol)) return xr;
            if(fa*fr<0){b=xr;fb=fr;}else{a=xr;fa=fr;}
            sebelumnya=xr;
        }
        return xr;
    }

    public static void main(String[] args) {
        try(Scanner sc=new Scanner(System.in)){
            System.out.println("=== METODE REGULAR FALSI ===");
            System.out.println("1. x^3 - x - 2\\n2. x^2 - 4\\n3. cos(x) - x (radian)\\n4. e^x - 3x\\n5. x^2 - x - 2");
            System.out.print("Pilih fungsi (1-5): "); int n=Integer.parseInt(sc.nextLine().trim());
            Fungsi f=pilih(n);
            System.out.print("Batas bawah a: "); double a=Double.parseDouble(sc.nextLine().trim());
            System.out.print("Batas atas b: "); double b=Double.parseDouble(sc.nextLine().trim());
            System.out.print("Toleransi (mis. 0.0001): "); double tol=Double.parseDouble(sc.nextLine().trim());
            System.out.print("Maksimal iterasi (1-1000): "); int maks=Integer.parseInt(sc.nextLine().trim());
            if(a>=b||tol<=0||!Double.isFinite(tol)||maks<1||maks>1000)
                throw new IllegalArgumentException("Periksa interval, toleransi, dan maksimal iterasi.");
            double akar=regulaFalsi(f,a,b,tol,maks);
            System.out.printf("%nPendekatan akar = %.10f%n",akar);
        }catch(NumberFormatException e){System.out.println("Input harus berupa angka yang valid.");}
        catch(IllegalArgumentException|ArithmeticException e){System.out.println("Kesalahan: "+e.getMessage());}
    }
}
