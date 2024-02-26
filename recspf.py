import dns.resolver

def get_spf_ips(domain, max_recursions=10):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for answer in answers:
            txt_record = answer.to_text()
            if 'v=spf1' in txt_record.lower():
                spf_parts = txt_record.split(' ')
                for part in spf_parts:
                    if part.startswith('ip4:') or part.startswith('ip6:'):
                        yield part[4:]
                    elif part.startswith('include:'):
                        included_domain = part[8:]
                        if max_recursions > 0:
                            yield from get_spf_ips(included_domain, max_recursions - 1)
    except dns.resolver.NXDOMAIN:
        pass

if __name__ == '__main__':
    target_domain = 'google.com.au' # to be replaced with argparser, or your target domain
    spf_ips = list(get_spf_ips(target_domain))
    if spf_ips:
        print(f"IP addresses in SPF records for {target_domain}:")
        for ip in spf_ips:
            print(ip)
    else:
        print(f"No SPF records found for {target_domain}.")
